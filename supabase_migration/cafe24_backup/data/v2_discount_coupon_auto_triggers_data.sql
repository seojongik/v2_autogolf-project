-- Table: v2_discount_coupon_auto_triggers
-- Backup Date: 2025-11-27T21:08:20.307420
-- Row Count: 5

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_discount_coupon_auto_triggers`;

INSERT INTO `v2_discount_coupon_auto_triggers` (`trigger_id`, `trigger_discription`, `trigger`, `filter1_table`, `filter1_field_name`, `filter1_new_data_is_`, `filter1_data`, `filter2_table`, `filter2_field_name`, `filter2_new_data_is_`, `filter2_data`, `updated_at`, `setting_status`, `branch_id`) VALUES (1, '평일 피크시간대 이용 고객 할인권', '특정시간대 이용', 'v2_priced_TS', 'day_of_week', '포함', '월,수,금,공휴일', 'v2_priced_TS', 'ts_start', '이상', '17:00', NULL, '유효', NULL);
INSERT INTO `v2_discount_coupon_auto_triggers` (`trigger_id`, `trigger_discription`, `trigger`, `filter1_table`, `filter1_field_name`, `filter1_new_data_is_`, `filter1_data`, `filter2_table`, `filter2_field_name`, `filter2_new_data_is_`, `filter2_data`, `updated_at`, `setting_status`, `branch_id`) VALUES (2, '90분 이상 집중연습', '타석이용', 'v2_priced_TS', 'ts_min', '이상', '90', NULL, NULL, NULL, NULL, NULL, '유효', NULL);
INSERT INTO `v2_discount_coupon_auto_triggers` (`trigger_id`, `trigger_discription`, `trigger`, `filter1_table`, `filter1_field_name`, `filter1_new_data_is_`, `filter1_data`, `filter2_table`, `filter2_field_name`, `filter2_new_data_is_`, `filter2_data`, `updated_at`, `setting_status`, `branch_id`) VALUES (3, '방문 횟수 혜택', '타석이용', 'v2_priced_TS', 'ts_min', '이상', '30', 'v2_priced_TS', 'member_type', '불포함', '주니어', NULL, '유효', NULL);
INSERT INTO `v2_discount_coupon_auto_triggers` (`trigger_id`, `trigger_discription`, `trigger`, `filter1_table`, `filter1_field_name`, `filter1_new_data_is_`, `filter1_data`, `filter2_table`, `filter2_field_name`, `filter2_new_data_is_`, `filter2_data`, `updated_at`, `setting_status`, `branch_id`) VALUES (4, '프로그램 이용고객 할인권', '프로그램 예약', 'v2_priced_TS', 'ts_min', '일치', '55', NULL, NULL, NULL, NULL, NULL, '유효', NULL);
INSERT INTO `v2_discount_coupon_auto_triggers` (`trigger_id`, `trigger_discription`, `trigger`, `filter1_table`, `filter1_field_name`, `filter1_new_data_is_`, `filter1_data`, `filter2_table`, `filter2_field_name`, `filter2_new_data_is_`, `filter2_data`, `updated_at`, `setting_status`, `branch_id`) VALUES (5, '120분 이상 집중연습', '타석이용', 'v2_priced_TS', 'ts_min', '이상', '120', NULL, NULL, NULL, NULL, NULL, '유효', NULL);

SET FOREIGN_KEY_CHECKS=1;
