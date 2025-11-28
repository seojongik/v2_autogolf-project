-- Table: v2_cancellation_policy
-- Backup Date: 2025-11-27T21:08:20.058285
-- Row Count: 27

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_cancellation_policy`;

INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bills', '선불크레딧', 3, '360', '50');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_times', '시간권', 3, '60', '30');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_games', '게임권', 3, '180', '10');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_LS_countings', '레슨권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_program_settings', '프로그램', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bills', '선불크레딧', 4, '1000', '10');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bills', '선불크레딧', 2, '180', '80');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bills', '선불크레딧', 1, '0', '95');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_times', '시간권', 2, '30', '80');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_times', '시간권', 4, '90', '10');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_times', '시간권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_games', '게임권', 2, '60', '20');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_bill_games', '게임권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('test', 'v2_program_settings', '프로그램', 2, '120', '50');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bill_times', '시간권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bill_games', '게임권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_LS_contracts', '레슨권', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_program_settings', '프로그램', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bill_times', '시간권', 2, '180', '60');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bill_games', '게임권', 2, '180', '50');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_LS_contracts', '레슨권', 2, '180', '50');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_program_settings', '프로그램', 2, '180', '50');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bills', '선불크레딧', 1, '0', '100');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bill_times', '시간권', 3, '30', '90');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bills', '선불크레딧', 2, '10', '90');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bills', '선불크레딧', 3, '110', '30');
INSERT INTO `v2_cancellation_policy` (`branch_id`, `db_table`, `service_category`, `apply_sequence`, `_min_before_use`, `penalty_percent`) VALUES ('famd', 'v2_bills', '선불크레딧', 4, '40', '60');

SET FOREIGN_KEY_CHECKS=1;
