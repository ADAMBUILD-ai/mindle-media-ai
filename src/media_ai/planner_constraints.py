"""Conservative checks on generated values; never a substitute plan generator."""
import math
import re

FIELDS = {'brightness': r'밝기|밝게|brightness', 'contrast': r'대비|contrast', 'saturation': r'채도|saturation'}
MEDIA_TOOL_FIELDS = {'speed', 'start', 'duration', 'aspect', 'fade', 'backgroundVolume'}
NEGATION = r'지\s*마|말|않|금지|유지|그대로|하지|do not|don.t|unchanged'
QUOTED = r'"[^"\n]*"|“[^”\n]*”|\'[^\'\n]*\''

def instruction_text(command):
    # Narration numbers and edit words are content, not editing instructions.
    return re.sub(QUOTED, '', command).casefold()

def requested_edit_fields(command):
    text = instruction_text(command)
    mentions = list(re.finditer("|".join("(?:"+p+")" for p in FIELDS.values()), text))
    return {next(key for key, pattern in FIELDS.items() if re.fullmatch(pattern, match.group()))
            for index, match in enumerate(mentions)
            if not re.search(NEGATION,
                text[match.end():mentions[index+1].start() if index+1 < len(mentions) else len(text)])}

def validate_edit_values(command, steps):
    text = instruction_text(command)
    mentions = list(re.finditer('|'.join('(?:'+p+')' for p in FIELDS.values()), text))
    expected = {}
    actual = {}
    for step in steps:
        if step['operation'] != 'video_edit':
            continue
        for key, value in step.get('options', {}).items():
            if key not in FIELDS:
                continue
            if key in actual:
                raise ValueError('PLANNER_DUPLICATE_EDIT: 같은 보정을 중복 실행할 수 없습니다.')
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError('PLANNER_VALUE_MISMATCH: 유한한 숫자 보정값이 필요합니다.')
            actual[key] = value
    for index, match in enumerate(mentions):
        field = next(key for key, pattern in FIELDS.items() if re.fullmatch(pattern, match.group()))
        clause = text[match.end():mentions[index+1].start() if index+1 < len(mentions) else len(text)]
        if field in expected:
            raise ValueError('PLANNER_AMBIGUOUS_VALUE: 같은 보정을 반복 지정했습니다. 한 번씩 명시하세요.')
        if re.search(NEGATION, clause):
            expected[field] = None
            continue
        if field not in actual:
            raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 영상 보정이 누락됐습니다.')
        if re.search(r'설정|맞춰|맞추|으로|로\s*(?:해|변경)|set\b', clause) or re.search(r'\d\s*(?:배|%|퍼센트|초|분|도|px|[eE][+-]?\d)', clause):
            raise ValueError('PLANNER_UNSUPPORTED_UNIT: 절대값·배율·백분율 설정은 지원하지 않습니다. 보정 포인트와 증감 방향을 명시하세요.')
        numbers = re.findall(r'(?<![\w.])[+-]?\d+(?:\.\d+)?(?![\d.])', clause)
        up = bool(re.search(r'높|올|증가|increase|raise', clause))
        down = bool(re.search(r'낮|내려|내리|줄|감소|decrease|lower|reduce', clause))
        if len(numbers) != 1 or up == down:
            raise ValueError('PLANNER_AMBIGUOUS_VALUE: 보정마다 숫자와 높이기·낮추기를 명시하세요.')
        value = float(numbers[0])
        if value < 0 or not 0 <= value <= 100:
            raise ValueError('PLANNER_UNSUPPORTED_VALUE: 0~100의 크기와 증감 방향을 별도로 명시하세요.')
        expected[field] = -value if down else value
    for key, value in expected.items():
        if value is None:
            if key in actual:
                raise ValueError('PLANNER_NEGATED_EDIT: 변경하지 말라는 보정이 포함됐습니다.')
        elif key not in actual or not math.isclose(actual[key], value, rel_tol=0, abs_tol=1e-9):
            raise ValueError('PLANNER_VALUE_MISMATCH: 요청한 보정 수치·증감 방향과 계획이 다릅니다.')
    return {key: value for key, value in expected.items() if value is not None}


def requested_media_tool_fields(command):
    text = instruction_text(command)
    requested = set()
    if re.search(r'속도|배속|speed', text):
        requested.add('speed')
    if re.search(r'자르|구간|trim', text):
        requested.update(('start', 'duration'))
    if re.search(r'(?:9\s*:\s*16|16\s*:\s*9)', text):
        requested.add('aspect')
    if re.search(r'페이드|fade', text):
        requested.add('fade')
    if re.search(r'배경\s*음악|bgm', text):
        requested.add('backgroundVolume')
    return requested


def validate_media_tool_values(command, steps):
    """Bind generated FFmpeg tool values to explicit user language."""
    text = instruction_text(command)
    expected = {}
    requested = requested_media_tool_fields(command)
    actual = {}
    bgm_location = None
    for step in steps:
        if step['operation'] == 'video_edit':
            for key, value in step.get('options', {}).items():
                if key not in MEDIA_TOOL_FIELDS:
                    continue
                if key in actual:
                    raise ValueError('PLANNER_DUPLICATE_TOOL: 같은 편집 도구를 중복 실행할 수 없습니다.')
                actual[key] = value
                if key == 'backgroundVolume':
                    bgm_location = 'video_edit'
        if step['operation'] == 'mix_narration' and 'background_volume' in step:
            if 'backgroundVolume' in actual:
                raise ValueError('PLANNER_DUPLICATE_TOOL: 배경음악은 한 번만 합성해야 합니다.')
            actual['backgroundVolume'] = step['background_volume']
            bgm_location = 'mix_narration'

    if 'speed' in requested:
        match = re.search(r'(?:속도|배속|speed)[^,.;\n]{0,24}?([0-9]+(?:\.[0-9]+)?)\s*(?:배|x)', text)
        if not match:
            raise ValueError('PLANNER_AMBIGUOUS_SPEED: 0.5~2배의 속도를 명시하세요.')
        expected['speed'] = float(match.group(1))
        if not .5 <= expected['speed'] <= 2:
            raise ValueError('PLANNER_UNSUPPORTED_SPEED: 속도는 0.5~2배입니다.')

    if {'start', 'duration'} & requested:
        match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*초\s*부터\s*([0-9]+(?:\.[0-9]+)?)\s*초\s*까지', text)
        if not match:
            raise ValueError('PLANNER_AMBIGUOUS_TRIM: 시작 초와 종료 초를 모두 명시하세요.')
        start, end = map(float, match.groups())
        if start < 0 or end <= start:
            raise ValueError('PLANNER_UNSUPPORTED_TRIM: 종료 초는 시작 초보다 커야 합니다.')
        expected.update(start=start, duration=end-start)

    if 'aspect' in requested:
        match = re.search(r'(9\s*:\s*16|16\s*:\s*9)', text)
        expected['aspect'] = match.group(1).replace(' ', '')
    if 'fade' in requested:
        expected['fade'] = True
    if 'backgroundVolume' in requested:
        match = re.search(r'(?:배경\s*음악|bgm)[^,.;\n]{0,24}?([0-9]+(?:\.[0-9]+)?)\s*%', text)
        expected['backgroundVolume'] = float(match.group(1))/100 if match else .35
        if not 0 <= expected['backgroundVolume'] <= 1:
            raise ValueError('PLANNER_UNSUPPORTED_BGM_VOLUME: 배경음악 음량은 0~100%입니다.')

    invented = set(actual) - requested
    if invented:
        raise ValueError('PLANNER_SCOPE_MISMATCH: 요청하지 않은 영상 도구가 포함됐습니다.')
    missing = requested - set(actual)
    if missing:
        raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 영상 도구가 누락됐습니다.')
    has_narration = any(step['operation'] in {'narrate', 'mix_narration'} for step in steps)
    if 'backgroundVolume' in requested and bgm_location != ('mix_narration' if has_narration else 'video_edit'):
        raise ValueError('PLANNER_BGM_MIX_LOCATION_MISMATCH: 나레이션과 BGM은 한 번의 오디오 믹스로 합성해야 합니다.')
    for key, expected_value in expected.items():
        value = actual.get(key)
        if isinstance(expected_value, float):
            if type(value) not in (int, float) or not math.isclose(float(value), expected_value, rel_tol=0, abs_tol=1e-9):
                raise ValueError('PLANNER_TOOL_VALUE_MISMATCH: 요청한 편집 수치와 계획이 다릅니다.')
        elif value != expected_value:
            raise ValueError('PLANNER_TOOL_VALUE_MISMATCH: 요청한 편집 설정과 계획이 다릅니다.')
    return expected
