-- Table: v2_salary_pro
-- Backup Date: 2025-11-27T21:08:21.790938
-- Row Count: 1

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_salary_pro`;

INSERT INTO `v2_salary_pro` (`branch_id`, `pro_id`, `pro_name`, `year`, `month`, `salary_status`, `contract_type`, `salary_base`, `salary_hour`, `salary_per_lesson`, `salary_per_event`, `salary_per_promo`, `salalry_per_noshow`, `severance_pay`, `salary_total`, `four_insure`, `income_tax`, `business_income_tax`, `local_tax`, `other_deduction`, `deduction_sum`, `salary_net`, `updated_at`, `tax_status`, `tax_office`, `tax_office_mail`) VALUES ('test', 2, '원청서', 2025, '8', '세무사검토', '고용(4대보험)', 0, 0, 36000, 0, 0, 18000, 0, 54000, 121, 0, 0, 0, 0, 121, 53879, '2025-08-31T18:43:18', NULL, '가나다 세무사1', 'jongik.suh@gmail.com');

SET FOREIGN_KEY_CHECKS=1;
