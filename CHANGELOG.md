# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Note: PyVoicing is currently in alpha; the API is subject to change.

## [0.1.4] - 2025-12-25
### Added
- Shared spelling preference via Spelling.prefer_flat.
- Pitch.lilypond with English LilyPond note names.
- Pitch.freq and pitch/chroma spell/enharmonic helpers.
- Named methods for transposition and voicing operations.
- Pytest-based tests for core types.

### Changed
- Operator usage aligned with named methods (transpose/add/remove).
- Voicing.tones replaces chord-tone output from ~voicing; ~voicing now returns MIDI values.

## [0.1.3] - 2025-04-30
### Fixed
- Rest.__str__()

## [0.1.2] - 2025-04-30
### Added
- Voicings.Drop2/3/24
- Voicings.int_list

## [0.1.1] - 2025-04-29
### Fixed
- Corrected ABC notation parsing in Pitch.

## [0.1.0] - 2025-04-28
### Added
- Initial release.
