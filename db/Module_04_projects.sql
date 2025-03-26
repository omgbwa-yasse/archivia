CREATE TABLE `projects` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `owner_id` BIGINT NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `start_date` TIMESTAMP NOT NULL,
    `end_date` TIMESTAMP NULL,
    `version` INT NOT NULL DEFAULT 1,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_project_owner` (`owner_id`),
    INDEX `idx_project_created` (`created_by`),
    INDEX `idx_project_updated` (`updated_by`),
    INDEX `idx_project_deleted` (`deleted_by`),
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `project_members` (
    `project_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `role` VARCHAR(50) NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`project_id`, `user_id`),
    INDEX `idx_member_created` (`created_by`),
    INDEX `idx_member_updated` (`updated_by`),
    FOREIGN KEY (`project_id`) REFERENCES `projects`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `project_tasks` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `project_id` BIGINT NOT NULL,
    `parent_task_id` BIGINT,
    `title` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `status` ENUM('TO_DO', 'IN_PROGRESS', 'BLOCKED', 'REVIEW', 'DONE') NOT NULL,
    `priority` ENUM('LOW', 'MEDIUM', 'HIGH', 'URGENT') NOT NULL,
    `estimated_hours` DECIMAL(10,2),
    `start_date` TIMESTAMP NULL,
    `due_date` TIMESTAMP NULL,
    `completed_at` TIMESTAMP NULL,
    `assigned_to` BIGINT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    `version` INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    INDEX `idx_task_project` (`project_id`),
    INDEX `idx_task_parent` (`parent_task_id`),
    INDEX `idx_task_assigned` (`assigned_to`),
    INDEX `idx_task_created` (`created_by`),
    FOREIGN KEY (`project_id`) REFERENCES `projects`(`id`),
    FOREIGN KEY (`parent_task_id`) REFERENCES `project_tasks`(`id`), -- Correction: référence à project_tasks et non tasks
    FOREIGN KEY (`assigned_to`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `project_resources` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `project_id` BIGINT NOT NULL,
    `resource_type` ENUM('HUMAN', 'MATERIAL', 'FINANCIAL') NOT NULL,
    `user_id` BIGINT,
    `name` VARCHAR(190) NOT NULL,
    `description` TEXT,
    `quantity` INT,
    `unit_cost` DECIMAL(10,2),
    `start_date` TIMESTAMP NULL,
    `end_date` TIMESTAMP NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    `version` INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    INDEX `idx_resource_project` (`project_id`),
    INDEX `idx_resource_user` (`user_id`),
    FOREIGN KEY (`project_id`) REFERENCES `projects`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `task_dependencies` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `task_id` BIGINT NOT NULL,
    `depends_on_task_id` BIGINT NOT NULL,
    `dependency_type` ENUM('FINISH_TO_START', 'START_TO_START', 'FINISH_TO_FINISH', 'START_TO_FINISH') NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_task_dependency` (`task_id`, `depends_on_task_id`),
    INDEX `idx_dependency_task` (`task_id`),
    INDEX `idx_dependency_depends` (`depends_on_task_id`),
    FOREIGN KEY (`task_id`) REFERENCES `project_tasks`(`id`) ON DELETE CASCADE, -- Correction: référence à project_tasks
    FOREIGN KEY (`depends_on_task_id`) REFERENCES `project_tasks`(`id`) ON DELETE CASCADE, -- Correction: référence à project_tasks
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour les commentaires sur les tâches
CREATE TABLE `task_comments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `task_id` BIGINT NOT NULL,
    `comment` TEXT NOT NULL,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_by` BIGINT,
    `deleted_at` TIMESTAMP NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_comment_task` (`task_id`),
    INDEX `idx_comment_created` (`created_by`),
    FOREIGN KEY (`task_id`) REFERENCES `project_tasks`(`id`) ON DELETE CASCADE, -- Correction: référence à project_tasks
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`deleted_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour suivre le temps passé sur les tâches
CREATE TABLE `time_entries` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `task_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `hours_spent` DECIMAL(10,2) NOT NULL,
    `work_date` DATE NOT NULL,
    `description` TEXT,
    `created_by` BIGINT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_by` BIGINT,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_time_task` (`task_id`),
    INDEX `idx_time_user` (`user_id`),
    INDEX `idx_time_date` (`work_date`),
    FOREIGN KEY (`task_id`) REFERENCES `project_tasks`(`id`) ON DELETE CASCADE, -- Correction: référence à project_tasks
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`created_by`) REFERENCES `users`(`id`),
    FOREIGN KEY (`updated_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;