# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Add `sessions` field to `Activity` model for per-domain SMTP session deliverability info

### Changed

* Add `meta="datetime"` to `Activity.timestamp` field for proper datetime rendering

### Fixed

*

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
