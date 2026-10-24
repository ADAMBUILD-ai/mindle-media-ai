# MEDIA-owned external production assets

This directory contains the immutable identity registry and the narrow adapters
that turn approved external programs into auditable MINDLE MEDIA AI assets.
Registry presence is not runtime approval. Disabled entries remain fail-closed
until their exact bytes, license, target hardware, real execution, and output
quality are evidenced.

The first owned executable contract is the Blender camera render driver. It can
select only an existing camera and bounded render settings from a JSON request.
It cannot evaluate user Python or shell text. ComfyUI/Wan activation additionally
requires an official API workflow export whose bytes and allowed inputs are
pinned; no guessed workflow is stored here.
