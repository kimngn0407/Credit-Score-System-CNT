// API service for communicating with Spring Boot backend
import type { PredictInput, PredictOutput, Explanation, Recommendation, HistoryItem, MonitoringMetrics } from '@/types/index';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api';

// User types for authentication
export type UserDTO = {
	id?: number;
	username: string;
	fullName?: string;
	email?: string;
	role: string;
	passwordHash?: string;
	themePreference?: string;
	createdAt?: string;
};

export type RegisterRequest = {
	username: string;
	passwordHash: string;
	fullName?: string;
	email?: string;
	role?: string;
	themePreference?: string;
};

export type ApplicationDTO = {
	id?: number;
	userId: number;
	loanAmnt: number;
	personAge: number;
	personIncome: number;
	personHomeOwnership: string;
	loanIntent: string;
	cbPersonDefaultOnFile: string;
	personEmpLength?: number;
	cbPersonCredHistLength?: number;
	status?: string;
	createdAt?: string;
};

// Helper function for API calls
async function fetchAPI<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
	const url = `${API_BASE_URL}${endpoint}`;
	const config: RequestInit = {
		headers: {
			'Content-Type': 'application/json',
			...options.headers,
		},
		...options,
	};

	const response = await fetch(url, config);
	if (!response.ok) {
		throw new Error(`API Error: ${response.status} - ${response.statusText}`);
	}
	return response.json();
}

// Authentication APIs
export const register = async (user: RegisterRequest): Promise<UserDTO> => {
	try {
		return await fetchAPI('/users/register', {
			method: 'POST',
			body: JSON.stringify(user),
		});
	} catch (error) {
		console.error('Register API error:', error);
		throw error;
	}
};

export const login = async (username: string, password: string): Promise<UserDTO> => {
	try {
		return await fetchAPI('/users/login', {
			method: 'POST',
			body: JSON.stringify({ username, passwordHash: password }),
		});
	} catch (error) {
		console.error('Login API error:', error);
		throw error;
	}
};

// Main API object with all endpoints
export const Api = {
	// Application workflow - STANDARDIZED to use Java backend only
	createApplication: async (input: PredictInput & { userId: number }): Promise<ApplicationDTO> => {
		try {
			const dto: ApplicationDTO = {
				userId: input.userId,
				loanAmnt: input.loan_amnt,
				personAge: input.person_age,
				personIncome: input.person_income,
				personHomeOwnership: input.person_home_ownership,
				loanIntent: input.loan_intent,
				cbPersonDefaultOnFile: input.cb_person_default_on_file,
				personEmpLength: input.person_emp_length,
				cbPersonCredHistLength: input.cb_person_cred_hist_length,
			};
			return await fetchAPI(`/applications/${input.userId}`, {
				method: 'POST',
				body: JSON.stringify(dto),
			});
		} catch (error) {
			console.error('CreateApplication API error:', error);
			throw error;
		}
	},

	runInference: async (applicationId: number): Promise<{ runId: number }> => {
		try {
			return await fetchAPI(`/inference/run/${applicationId}`, {
				method: 'POST',
			});
		} catch (error) {
			console.error('RunInference API error:', error);
			throw error;
		}
	},

	getPredictions: async (runId: number): Promise<Array<{
		decision: string;
		probability_approve: number;
		probability_reject: number;
		credit_score: number;
	}>> => {
		try {
			return await fetchAPI(`/predictions/run/${runId}`);
		} catch (error) {
			console.error('GetPredictions API error:', error);
			throw error;
		}
	},

	getExplanation: async (applicationId: number): Promise<Explanation> => {
		try {
			const explanation = await fetchAPI<{
				method: string;
				details?: Array<{
					featureName: string;
					featureValue: string;
					shapValue: number;
				}>;
			}>(`/explanations/application/${applicationId}`);
			
			if (!explanation || !Array.isArray(explanation.details)) {
				return { method: (explanation?.method as Explanation['method']) || 'SHAP', features: [] };
			}
			return {
				method: explanation.method as Explanation['method'],
				features: explanation.details.map(detail => ({
					name: detail.featureName,
					value: detail.featureValue,
					shap: detail.shapValue,
				})),
			};
		} catch (error) {
			console.error('Explanation API error:', error);
			return { method: 'SHAP', features: [] };
		}
	},

	getRecommendations: async (applicationId: number): Promise<Recommendation[]> => {
		try {
			const recommendations = await fetchAPI<Array<{
				recCode: string;
				message: string;
				expectedGain: number;
			}>>(`/recommendations/application/${applicationId}`);
			
			return recommendations.map(rec => ({
				rec_code: rec.recCode,
				message: rec.message,
				expected_gain: rec.expectedGain,
			}));
		} catch (error) {
			console.error('Recommendations API error:', error);
			return [];
		}
	},

	// History and Analytics
	getHistory: async (userId: string): Promise<HistoryItem[]> => {
		try {
			const history = await fetchAPI<Array<{
				id: number;
				createdAt: string;
				decision: string;
				creditScore: number;
				loanAmnt: number;
			}>>(`/applications/user/${userId}`);
			
			return history.map(item => ({
				date: new Date(item.createdAt).toISOString().split('T')[0],
				score: item.creditScore,
				decision: item.decision.toLowerCase() as 'approve' | 'reject' | 'pending',
			}));
		} catch (error) {
			console.error('History API error:', error);
			return [];
		}
	},

	getDashboardSummary: async () => {
		try {
			const summary = await fetchAPI<{
				totalApplications: number;
				approvedCount: number;
				rejectedCount: number;
				averageScore: number;
			}>('/dashboard/summary');
			
			return {
				pie: [
					{ name: 'Approve', value: summary.approvedCount },
					{ name: 'Reject', value: summary.rejectedCount },
				],
				bar: [
					{ name: 'Total Applications', value: summary.totalApplications },
					{ name: 'Average Score', value: summary.averageScore },
				],
				line: [],
			};
		} catch (error) {
			console.error('Dashboard API error:', error);
			return {
				pie: [
					{ name: 'Approve', value: 0 },
					{ name: 'Reject', value: 0 },
				],
				bar: [],
				line: [],
			};
		}
	},

	getMonitoringMetrics: async (): Promise<MonitoringMetrics> => {
		try {
			const metrics = await fetchAPI<{
				accuracyOverTime: Array<{
					date: string;
					accuracy: number;
				}>;
			}>('/monitoring/metrics');
			
			return {
				accuracyOverTime: metrics.accuracyOverTime.map(item => ({
					name: item.date,
					value: item.accuracy,
				})),
			};
		} catch (error) {
			console.error('Monitoring API error:', error);
			return { accuracyOverTime: [] };
		}
	},
};