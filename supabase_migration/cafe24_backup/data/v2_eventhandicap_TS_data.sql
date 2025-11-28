-- Table: v2_eventhandicap_TS
-- Backup Date: 2025-11-27T21:08:20.408730
-- Row Count: 5

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_eventhandicap_TS`;

INSERT INTO `v2_eventhandicap_TS` (`branch_id`, `ts_date`, `ts_payment_method`, `ts_status`, `member_id`, `member_type`, `member_name`, `member_phone`, `ts_min`, `time_stamp`, `memo`) VALUES ('test', '2025-09-06', '이벤트선정 차감', '결제완료', 901, '웰빙클럽', '서종익', '010-6250-7373', 50, '2025-09-06T14:24:50', '테스트');
INSERT INTO `v2_eventhandicap_TS` (`branch_id`, `ts_date`, `ts_payment_method`, `ts_status`, `member_id`, `member_type`, `member_name`, `member_phone`, `ts_min`, `time_stamp`, `memo`) VALUES ('test', '2025-09-06', '이벤트선정 차감', '결제완료', 901, '웰빙클럽', '서종익', '010-6250-7373', -120, '2025-09-06T14:34:29', '2차 이벤트');
INSERT INTO `v2_eventhandicap_TS` (`branch_id`, `ts_date`, `ts_payment_method`, `ts_status`, `member_id`, `member_type`, `member_name`, `member_phone`, `ts_min`, `time_stamp`, `memo`) VALUES ('test', '2025-09-06', '이벤트선정 차감', '결제완료', 903, '주니어', '서재우', '010-6565-0876', -30, '2025-09-06T14:42:20', '이벤트');
INSERT INTO `v2_eventhandicap_TS` (`branch_id`, `ts_date`, `ts_payment_method`, `ts_status`, `member_id`, `member_type`, `member_name`, `member_phone`, `ts_min`, `time_stamp`, `memo`) VALUES ('test', '2025-09-07', '이벤트선정 차감', '결제완료', 901, '웰빙클럽', '서종익', '010-6250-7373', -50, '2025-09-07T21:41:40', '차감');
INSERT INTO `v2_eventhandicap_TS` (`branch_id`, `ts_date`, `ts_payment_method`, `ts_status`, `member_id`, `member_type`, `member_name`, `member_phone`, `ts_min`, `time_stamp`, `memo`) VALUES ('test', '2025-09-07', '이벤트선정 보너스', '결제완료', 901, '웰빙클럽', '서종익', '010-6250-7373', 120, '2025-09-07T21:48:05', '12345');

SET FOREIGN_KEY_CHECKS=1;
