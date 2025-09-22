-- Flyway Migration: Initial schema

-- 1) User & Role Management
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('USER','STAFF','ADMIN')),
    theme_preference VARCHAR(10) DEFAULT 'light',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2) Hồ sơ vay
CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    person_age INT NOT NULL,
    person_income NUMERIC(12,2) NOT NULL,
    loan_amnt NUMERIC(12,2) NOT NULL,
    person_home_ownership VARCHAR(20) NOT NULL,
    cb_person_default_on_file CHAR(1) NOT NULL,
    loan_intent VARCHAR(30) NOT NULL,
    person_emp_length NUMERIC(5,2),
    cb_person_cred_hist_length INT,
    status VARCHAR(24) DEFAULT 'PENDING_INFERENCE',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3) Inference runs
CREATE TABLE IF NOT EXISTS inference_runs (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT now(),
    finished_at TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'RUNNING',
    model_version VARCHAR(32) NOT NULL
);

-- 4) Predictions
CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    inference_run_id BIGINT REFERENCES inference_runs(id) ON DELETE CASCADE,
    decision VARCHAR(10) NOT NULL,
    probability_approve NUMERIC(6,4) NOT NULL,
    probability_reject NUMERIC(6,4) NOT NULL,
    credit_score INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5) Explanations
CREATE TABLE IF NOT EXISTS explanations (
    id BIGSERIAL PRIMARY KEY,
    inference_run_id BIGINT REFERENCES inference_runs(id) ON DELETE CASCADE,
    method VARCHAR(16) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS explanation_details (
    id BIGSERIAL PRIMARY KEY,
    explanation_id BIGINT REFERENCES explanations(id) ON DELETE CASCADE,
    feature_name VARCHAR(64) NOT NULL,
    feature_value TEXT,
    shap_value NUMERIC(12,6) NOT NULL,
    contribution_pct NUMERIC(6,2),
    rank INT NOT NULL
);

-- 6) Recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id BIGSERIAL PRIMARY KEY,
    inference_run_id BIGINT REFERENCES inference_runs(id) ON DELETE CASCADE,
    rec_code VARCHAR(32) NOT NULL,
    message TEXT NOT NULL,
    expected_gain NUMERIC(6,2),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 7) Credit history
CREATE TABLE IF NOT EXISTS credit_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    date TIMESTAMPTZ DEFAULT now(),
    score INT NOT NULL,
    decision VARCHAR(10) NOT NULL
);

-- 8) Blockchain hashes
CREATE TABLE IF NOT EXISTS blockchain_hashes (
    id BIGSERIAL PRIMARY KEY,
    inference_run_id BIGINT REFERENCES inference_runs(id) ON DELETE CASCADE,
    hash_value VARCHAR(256) NOT NULL,
    chain_ref TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 9) Prediction logs
CREATE TABLE IF NOT EXISTS prediction_logs (
    id BIGSERIAL PRIMARY KEY,
    inference_run_id BIGINT REFERENCES inference_runs(id) ON DELETE CASCADE,
    input_payload JSONB,
    output_payload JSONB,
    latency_ms INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 10) Model monitoring
CREATE TABLE IF NOT EXISTS model_monitoring (
    id BIGSERIAL PRIMARY KEY,
    model_version VARCHAR(32),
    accuracy NUMERIC(5,2),
    auc NUMERIC(5,2),
    drift_score NUMERIC(5,2),
    measured_at TIMESTAMPTZ DEFAULT now()
);

-- 11) Customer locations
CREATE TABLE IF NOT EXISTS customer_locations (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT REFERENCES applications(id) ON DELETE CASCADE,
    province VARCHAR(64) NOT NULL,
    district VARCHAR(64),
    lat NUMERIC(9,6),
    lon NUMERIC(9,6)
);


