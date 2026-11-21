# What ridni.app promises, and where the code keeps it

Every statement on the privacy, delete-account, support and terms pages that says what the
app does with data is listed here with the file that makes it true. Audited against the code
on 2026-11-20 (app `family-app-rn`, backend `family-app/backend`).

**Rule.** A change in the app or backend that touches any row below updates this file and the
page text in all 7 languages (`_build/pages/<lang>/`) in the same piece of work, then
`python3 _build/build.py`. The pages are written from this file and the code, never from
design handoff docs alone. A row whose status is not ✅ is a promise the code does not keep yet.

| # | Claim on the site | Where it is true | Status |
|---|---|---|---|
| 1 | Records: sleep, feeds, drinks, diapers, pumping, baths, walks, teething, activities; weight, height, head; notes, temperature, meds, vaccinations, appointments; pregnancy; mother's weight & height; cycle | app `src/store/api/*Api.ts`; backend `app/models/` | ✅ |
| 2 | Only family adults see records; no public link | backend `app/services/family.py`, `cycle_privacy.py`, `mother_privacy.py` | ✅ |
| 3 | Caregiver does not see cycle, pregnancy, mother's weight, her appointments | backend `app/services/cycle_privacy.py`, `mother_privacy.py` | ✅ |
| 4 | Mother's weight visible to other adults only after `share_weight` | backend `app/services/mother_privacy.py` | ✅ |
| 5 | Account: name, email, photo, password hash; Google/Apple id; Apple token for revocation; region, tz, units, language, theme, cycle goal | backend `app/models/user.py` | ✅ |
| 6 | Per phone: platform, app version, last sync, push token | backend `app/models/sync.py` (`SyncDevice`); app `src/services/appVersion.ts` (bundle version + build via `react-native-device-info`), sent by `src/hooks/useSyncManager.ts` | ✅ (S-295) |
| 7 | Child: name, nickname, birth date/time, gender, birth details, blood type, notes, photo, measurements | backend `app/models/child.py`; app `src/store/api/childrenApi.ts` | ✅ |
| 8 | Photos: camera or library, one picked photo, not saved to gallery, 256×256 JPEG ≤100 KB, stored in DB, family-only, child photo by owner/parent, adult photo by self | app `src/components/features/PhotoAvatarControl.tsx`; backend `app/models/profile_photo.py`, `app/api/v1/photos.py` | ✅ |
| 9 | Photo deleted on remove, with child profile, with account | backend `app/services/profile_photo.py`, `account.py::anonymize_user`, `workers/tasks/purge.py::purge_orphan_photos` | ✅ |
| 10 | 18+ to create an account | app `src/features/auth/components/AgeAndTermsNotice.tsx` | ✅ |
| 11 | Cycle visible only to its owner until sharing is on; reminders computed on phone | backend `app/services/cycle_privacy.py`; app notifee scheduling | ✅ |
| 12 | WHO band on growth chart; IOM range on pregnancy weight chart; no verdicts | app `src/features/records/utils/iomBand.ts`, growth chart | ✅ |
| 13 | Doctor PDF made on the phone, shared by the user, consent each time | app `src/features/health/share/pdf/*`, `SharePdfConsentDialog.tsx` | ✅ |
| 14 | Emails: verify, reset, email change (+ notice to old address), deletion scheduled, deletion done; via Resend from noreply@mail.ridni.app | backend `app/emails/templates.py` (`EmailKind`) | ✅ |
| 15 | Push via APNs / FCM; daily summary and "timer stopped" from server | backend `app/workers/main.py` | ✅ |
| 16 | Crashlytics: device model, OS, stack, installation id; no name/email/records; fatal and unhandled errors | app `src/services/crashReporting.ts` (`toError`: error type + message only, payloads dropped; the only file importing Crashlytics — `src/services/__tests__/crashReporting.test.ts`) | ✅ (S-295) |
| 17 | No ads, no analytics SDK, no location | app `package.json`, `ios/Ridni/Info.plist`, `AndroidManifest.xml` | ✅ |
| 18 | Server logs: failed/slow/sign-in/setup requests; account id, path, status, time; no IP, no body; deleted after 90 days | backend `app/core/logging_middleware.py`, `app/models/api_log.py`; daily purge `app/workers/tasks/cleanup.py::purge_old_api_logs` (04:45 UTC, `config.api_log_retention_days` = 90) | ✅ (S-295) |
| 19 | Hosting DigitalOcean Frankfurt; Resend EU; Firebase; Apple; Google | infrastructure (`docs/plans/05-…-RESULTS.md`) | ✅ |
| 20 | Deleted record: soft delete, hard delete after 30 days | backend `app/workers/tasks/purge.py` (docstring: 30 days, separate from the 7-day account recovery), `config.soft_delete_retention_days` | ✅ (S-295) |
| 21 | Account deletion: 7-day grace, then anonymise (name, email, password, tokens, push, notification settings, OAuth revoked) | backend `app/api/v1/users.py`, `workers/tasks/account_cleanup.py`, `services/account.py` | ✅ |
| 22 | Deleted with account: cycle, own weight/height, appointments, pumping, pregnancy entries made, photo, devices | backend `services/account.py::delete_personal_data` (CASCADE FKs to `users`) | ✅ |
| 23 | Ownership passes to the longest-standing parent; last adult takes the family with them | backend `services/family.py::release_families_of_departing_user`; also when an owner leaves to join another family as a parent (`services/family.py::accept_invitation`, mode `leave`, D-252) | ✅ |
| 24 | Backups kept ≤ 7 days | DigitalOcean database settings | check with owner |
| 25 | Family code: 6 characters (letters and digits), valid 7 days | backend `app/models/family.py`, `config.invitation_expire_days` | ✅ |
| 26 | Timer lock lifts after 30 minutes | backend `app/core/timer_locks.py` | ✅ |
| 27 | Delete account asks to type DELETE | app `DeleteAccountScreen` | ✅ |
| 28 | No export button | app | ✅ (PDF is per child, health only) |
| 29 | An adult is a parent in one family only; a caregiver may be in several families, with a role per family | backend `services/family.py::adult_membership`, `ensure_not_adult_elsewhere`, `_path_for` (D-252) | ✅ |
| 30 | (not on the pages yet) A parent invited into another family who is the only adult in their own can merge: after a page listing what moves, their children and every record move into the inviting family under the same dates, and their own family is dissolved; a child with the same name and birth date is joined only if they say so | backend `services/family_merge.py` (MOVES / LEAVES, swept by `tests/integration/test_family_merge_sweep.py`) | ✅ |
| 31 | A push names its family when the person is in more than one | backend `services/notification.py::_send_naming_family` | ✅ |
| 32 | Lock Screen / Dynamic Island while a sleep runs (Live Activity) and the Home widget show the least identifying thing: with one child no identity at all; with several, the avatar colour + initial; the child's name only if the parent turns it on in Privacy; never a photo. Their data stays on the phone (App Group container) | app `ios/RidniWidgets/*` (IdentityMark), `src/features/widgets/*`, `PrivacyScreen` toggle `settings.privacy.lockScreenName` (D-257, S-298) — shipped in 0.1 (30) | ✅ |
