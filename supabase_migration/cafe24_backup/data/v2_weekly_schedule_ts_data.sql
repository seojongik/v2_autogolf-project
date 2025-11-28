-- Table: v2_weekly_schedule_ts
-- Backup Date: 2025-11-27T21:08:22.328141
-- Row Count: 16

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_weekly_schedule_ts`;

INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '일요일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '월요일', 'close', NULL, NULL, '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '화요일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '수요일', 'close', NULL, NULL, '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '목요일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '금요일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '토요일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('test', '공휴일', 'open', '9:00:00', '22:00:00', '2025-08-02T19:56:42');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '일요일', 'open', '7:00:00', '22:00:00', '2025-09-23T22:43:16');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '월요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:16');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '화요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:16');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '수요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:16');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '목요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:17');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '금요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:17');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '토요일', 'open', '6:00:00', '0:00:00', '2025-09-23T22:43:17');
INSERT INTO `v2_weekly_schedule_ts` (`branch_id`, `day_of_week`, `is_holiday`, `business_start`, `business_end`, `updated_at`) VALUES ('famd', '공휴일', 'open', '7:00:00', '22:00:00', '2025-09-23T22:43:17');

SET FOREIGN_KEY_CHECKS=1;
