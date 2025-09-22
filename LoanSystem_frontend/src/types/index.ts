export type PredictInput = {
	person_age: number;
	person_income: number;
	loan_amnt: number;
	person_home_ownership: string;
	cb_person_default_on_file: 'Y' | 'N';
	loan_intent: string;
	person_emp_length?: number;
	cb_person_cred_hist_length?: number;
};

export type PredictOutput = {
	decision: 'approve' | 'reject';
	probability: number; // 0..1
	credit_score: number; // 0..1000
	trend?: { date: string; score: number; decision: 'approve' | 'reject' | 'pending' }[];
};

export type Explanation = {
	method: 'SHAP' | 'LIME' | 'RULES';
	features: { name: string; value?: string | number; shap?: number; contribution_pct?: number }[];
};

export type Recommendation = {
	rec_code: string;
	message: string;
	expected_gain?: number;
};

export type HistoryItem = {
	date: string;
	score: number;
	decision: 'approve' | 'reject' | 'pending';
};

export type MonitoringMetrics = {
	apiLatencyMs?: number[];
	accuracyOverTime?: { name: string; value: number }[];
	modelVersion?: string;
};


