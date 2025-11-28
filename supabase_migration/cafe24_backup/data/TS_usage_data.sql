-- Table: TS_usage
-- Backup Date: 2025-11-27T21:08:16.017507
-- Row Count: 1

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `TS_usage`;

INSERT INTO `TS_usage` (`ts_id`, `member_id`, `ts_date`, `ts_start`, `ts_end`, `ts_type`, `ts_min`, `morning_min`, `normal_min`, `peak_min`, `night_min`, `total_amt`, `term_discount`, `junior_discount`, `overtime_discount`, `revisit_discount_today`, `total_discount`, `net_amt`, `reservation_id`, `branch_id`) VALUES (2, 2, '2025-08-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '250801_2_0900', 'test');

SET FOREIGN_KEY_CHECKS=1;
