"""Conservative checks on generated values; never a substitute plan generator."""
import math
import re

FIELDS = {'brightness': r'밝기|밝게|brightness', 'contrast': r'대비|contrast', 'saturation': r'채도|saturation'}
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
