# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*

### Changed

*

### Fixed

* Fix encoding mismatch in raw and HTML contents endpoints by using UTF-8 instead of default latin-1

## [0.7.1] - 2026-04-12

### Changed

* Add `meta="longtext"` to `Activity.contents` field for proper long text rendering
* Mark `Activity.contents` field as `private=True` to exclude from default queries
* Use `contents_size` to detect contents availability instead of loading the full field

## [0.7.0] - 2026-04-12

### Added

* Add `contents` field to `Activity` model for storing full raw email contents
* Add `MAILOG_STORE_CONTENTS` config option to control email contents storage
* Add raw and HTML contents viewer endpoints in delivery report
* Add `View Raw` and `View HTML` links in delivery report when contents are available

### Changed

* Update README with `MAILOG_STORE_CONTENTS` configuration entry

## [0.6.0] - 2026-04-12

### Added

* Add collapsible SMTP session transcript with directional arrows and millisecond timestamps

### Changed

* Refactor collapsible CSS classes from headers-specific to shared `report-collapsible` pattern

## [0.5.1] - 2026-04-12

### Changed

* Time resolution improved

## [0.5.0] - 2026-04-12

### Added

* Add SMTP capabilities display as badges in delivery report sessions
* Add session start and end timestamps to delivery report

### Changed

* Replace per-session message size with start/end time fields in session formatting

## [0.4.0] - 2026-04-12

### Added

* Add delivery report page with per-session TLS, timing, and recipient details
* Add `server_agent` field to `Activity` model for relay server identification
* Add `contents_size` field to `Activity` model for message size tracking
* Add `report.css` stylesheet for delivery report styling

### Changed

* Add `View Report` instance link to `Activity` model

## [0.3.0] - 2026-04-12

### Added

* Add `observations` to all `Activity` model fields for better documentation

## [0.2.0] - 2026-04-12

### Added

* Add `sessions` field to `Activity` model for per-domain SMTP session deliverability info

### Changed

* Add `meta="datetime"` to `Activity.timestamp` field for proper datetime rendering

## [0.1.1] - 2026-04-12

### Fixed

* Use `safe=False` in activity webhook endpoint so all fields are accepted from the JSON payload
* Add `_plural` override to `Activity` model to return "Activities" instead of "Activitys"

## [0.1.0] - 2026-04-11

### Added

* Initial project setup with Appier Admin infrastructure
* `Activity` model for storing SMTP relay delivery events
* `POST /api/activity` webhook endpoint with shared secret authentication
* CSV export link for activity records
