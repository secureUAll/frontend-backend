-- machines_machineworker
ALTER TABLE machines_machineworker ADD CONSTRAINT machine_machineworker_worker_cascade FOREIGN KEY (worker_id) REFERENCES workers_worker(id) ON DELETE CASCADE;
ALTER TABLE machines_machineworker DROP CONSTRAINT machines_machineworker_worker_id_fcab3733_fk_workers_worker_id;