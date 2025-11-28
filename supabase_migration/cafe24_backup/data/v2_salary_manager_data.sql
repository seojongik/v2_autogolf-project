-- Table: v2_salary_manager
-- Backup Date: 2025-11-27T21:08:21.758111
-- Row Count: 1

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_salary_manager`;

INSERT INTO `v2_salary_manager` (`branch_id`, `manager_id`, `manager_name`, `year`, `month`, `salary_status`, `contract_type`, `salary_base`, `salary_hour`, `severance_pay`, `salary_total`, `four_insure`, `income_tax`, `business_income_tax`, `local_tax`, `other_deduction`, `deduction_sum`, `salary_net`, `updated_at`, `tax_status`, `tax_office`, `tax_office_mail`) VALUES ('test', 2, '고민정', 2025, '8', '세무사검토', '프리랜서', 150000, 108000, 0, 268000, 0, 0, 121, 0, 212, 333, 267667, '2025-08-31T18:43:31', '', '가나다 세무사1', 'jongik.suh@gmail.com');

SET FOREIGN_KEY_CHECKS=1;
