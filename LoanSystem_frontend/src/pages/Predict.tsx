import { useState } from 'react';
import CreditHealthBar from '@/components/CreditHealthBar';
import LoanTimeline from '@/components/LoanTimeline';
import RoleWelcome from '@/components/RoleWelcome';
import { Api } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import type { PredictInput, PredictOutput, Explanation, Recommendation } from '../types';

const defaultInput: PredictInput = {
	person_age: 30,
	person_income: 625, // 625 USD instead of 15,000,000 VND
	loan_amnt: 2083, // 2083 USD instead of 50,000,000 VND
	person_home_ownership: 'RENT',
	cb_person_default_on_file: 'N',
	loan_intent: 'PERSONAL',
	person_emp_length: 3,
	cb_person_cred_hist_length: 5,
};

export default function Predict() {
	const { user } = useAuth();
	const [form, setForm] = useState<PredictInput>(defaultInput);
	const [result, setResult] = useState<PredictOutput | null>(null);
	const [explain, setExplain] = useState<Explanation | null>(null);
	const [recs, setRecs] = useState<Recommendation[]>([]);
	const [loading, setLoading] = useState(false);

	const handleChange = (key: keyof PredictInput, value: string | number) => {
		setForm(prev => ({ ...prev, [key]: typeof (prev as any)[key] === 'number' ? Number(value) : value } as PredictInput));
	};

	const submit = async () => {
		setLoading(true);
		try {
			const userId = user?.id;
			if (!userId) throw new Error('Không tìm thấy userId');

			// 1. Tạo application
			const application = await Api.createApplication({ ...form, userId: Number(userId) });
			const applicationId = application.id;
			if (!applicationId) throw new Error('Không tìm thấy applicationId');

			// 2. Chạy inference
			const inferenceResult = await Api.runInference(applicationId);
			const runId = inferenceResult.runId;
			if (!runId) throw new Error('Không tìm thấy runId');

			// 3. Lấy prediction (phòng thủ giá trị)
			const predictions = await Api.getPredictions(runId);
			if (predictions.length > 0) {
				const pred = predictions[0] as any;
				const pApprove = Number(pred?.probability_approve) || 0;
				const pReject = Number(pred?.probability_reject) || 0;
				const creditScore = Number(pred?.credit_score);
				const probabilityRaw = (String(pred?.decision).toUpperCase() === 'APPROVE') ? pApprove : pReject;
				const probability = Math.max(0, Math.min(1, probabilityRaw));
				setResult({
					decision: String(pred?.decision).toLowerCase() === 'approve' ? 'approve' : 'reject',
					probability,
					credit_score: Number.isFinite(creditScore) ? creditScore : 0,
				});
			} else {
				setResult({ decision: 'reject', probability: 0.42, credit_score: 420 });
			}

			// 4. Lấy explanation
			const exp = await Api.getExplanation(applicationId);
			setExplain(exp);

			// 5. Lấy recommendations
			const rs = await Api.getRecommendations(applicationId);
			setRecs(rs);
		} finally {
			setLoading(false);
		}
	};

	const formatCurrency = (amount: number) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0,
		}).format(amount);
	};

	return (
		<div className="space-y-8">
			{/* Role-based Welcome */}
			<RoleWelcome />

			{/* Header */}
			<div className="text-center py-8">
				<h1 className="text-4xl font-bold gradient-text mb-4">Dự đoán Tín dụng AI</h1>
				<p className="text-gray-600 dark:text-gray-400 text-lg">
					{user?.role === 'USER' 
						? 'Tạo hồ sơ vay mới và nhận dự đoán chính xác về khả năng duyệt vay'
						: user?.role === 'STAFF'
						? 'Đánh giá hồ sơ khách hàng và đưa ra quyết định duyệt vay'
						: 'Giám sát và phân tích toàn bộ quy trình dự đoán tín dụng'
					}
				</p>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
				{/* Input Form */}
				<section className="card-glass space-y-6">
					<div className="flex items-center gap-3 mb-6">
						<div className="icon-wrapper">
							<span className="text-xl">📝</span>
						</div>
						<div>
							<h2 className="h2-title mb-0">Thông tin hồ sơ</h2>
							<p className="text-sm text-gray-600 dark:text-gray-400">Điền đầy đủ thông tin để có kết quả chính xác</p>
						</div>
					</div>

					<div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
						{/* Personal Information */}
						<div className="space-y-4">
							<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
								<span className="text-primary">👤</span>
								Thông tin cá nhân
							</h3>
							
							<label className="flex flex-col gap-2">
								<span className="label-sm">Tuổi</span>
								<input 
									className="input-base" 
									type="number" 
									value={form.person_age}
									onChange={e => handleChange('person_age', e.target.value)}
									placeholder="Nhập tuổi"
								/>
							</label>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Thu nhập hàng tháng</span>
								<input 
									className="input-base" 
									type="number" 
									value={form.person_income}
									onChange={e => handleChange('person_income', e.target.value)}
									placeholder="Nhập thu nhập"
								/>
								<span className="text-xs text-gray-500">{formatCurrency(form.person_income)}</span>
							</label>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Số năm kinh nghiệm làm việc</span>
								<input 
									className="input-base" 
									type="number" 
									value={form.person_emp_length}
									onChange={e => handleChange('person_emp_length', e.target.value)}
									placeholder="Số năm"
								/>
							</label>
						</div>

						{/* Loan Information */}
						<div className="space-y-4">
							<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
								<span className="text-primary">💰</span>
								Thông tin khoản vay
							</h3>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Số tiền vay</span>
								<input 
									className="input-base" 
									type="number" 
									value={form.loan_amnt}
									onChange={e => handleChange('loan_amnt', e.target.value)}
									placeholder="Nhập số tiền vay"
								/>
								<span className="text-xs text-gray-500">{formatCurrency(form.loan_amnt)}</span>
							</label>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Mục đích vay</span>
								<select 
									className="input-base" 
									value={form.loan_intent}
									onChange={e => handleChange('loan_intent', e.target.value)}
								>
									<option value="PERSONAL">Cá nhân</option>
									<option value="EDUCATION">Giáo dục</option>
									<option value="MEDICAL">Y tế</option>
									<option value="VENTURE">Kinh doanh</option>
									<option value="HOMEIMPROVEMENT">Cải thiện nhà</option>
									<option value="DEBTCONSOLIDATION">Hợp nhất nợ</option>
								</select>
							</label>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Tình trạng nhà ở</span>
								<select 
									className="input-base" 
									value={form.person_home_ownership}
									onChange={e => handleChange('person_home_ownership', e.target.value)}
								>
									<option value="RENT">Thuê nhà</option>
									<option value="OWN">Sở hữu</option>
									<option value="MORTGAGE">Thế chấp</option>
									<option value="OTHER">Khác</option>
								</select>
							</label>
						</div>
					</div>

					{/* Credit Information */}
					<div className="space-y-4">
						<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
							<span className="text-primary">📊</span>
							Thông tin tín dụng
						</h3>

						<div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
							<label className="flex flex-col gap-2">
								<span className="label-sm">Lịch sử nợ xấu</span>
								<select 
									className="input-base" 
									value={form.cb_person_default_on_file}
									onChange={e => handleChange('cb_person_default_on_file', e.target.value)}
								>
									<option value="N">Không có nợ xấu</option>
									<option value="Y">Có nợ xấu</option>
								</select>
							</label>

							<label className="flex flex-col gap-2">
								<span className="label-sm">Độ dài lịch sử tín dụng (năm)</span>
								<input 
									className="input-base" 
									type="number" 
									value={form.cb_person_cred_hist_length}
									onChange={e => handleChange('cb_person_cred_hist_length', e.target.value)}
									placeholder="Số năm"
								/>
							</label>
						</div>
					</div>

					<button 
						onClick={submit} 
						disabled={loading} 
						className="btn-primary w-full py-4 text-lg"
					>
						{loading ? (
							<div className="flex items-center gap-2">
								<div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
								<span>Đang phân tích...</span>
							</div>
						) : (
							<div className="flex items-center gap-2">
								<span className="text-xl">🔮</span>
								<span>Dự đoán ngay</span>
							</div>
						)}
					</button>
				</section>

				{/* Results */}
				<section className="card-glass space-y-6">
					<div className="flex items-center gap-3 mb-6">
						<div className="icon-wrapper">
							<span className="text-xl">📊</span>
						</div>
						<div>
							<h2 className="h2-title mb-0">Kết quả dự đoán</h2>
							<p className="text-sm text-gray-600 dark:text-gray-400">Phân tích AI và khuyến nghị</p>
						</div>
					</div>

					{result ? (
						<div className="space-y-6">
							{/* Decision Card */}
							<div className={`p-6 rounded-2xl border-2 ${
								 result.decision === 'approve' 
								 ? 'border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-900/20' 
								 : 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20'
							}`}>
								<div className="flex items-center gap-4 mb-4">
									<div className={`icon-wrapper ${
										 result.decision === 'approve' 
										 ? 'bg-gradient-to-br from-blue-400 to-blue-600' 
										 : 'bg-gradient-to-br from-red-500 to-red-600'
									}`}>
										<span className="text-2xl">
											 {result.decision === 'approve' ? '✅' : '❌'}
										</span>
									</div>
									<div>
										<h3 className="text-2xl font-bold">
											 {result.decision === 'approve' ? 'ĐƯỢC DUYỆT' : 'BỊ TỪ CHỐI'}
										</h3>
										<p className="text-sm text-gray-600 dark:text-gray-400">
									{(() => {
										const prob = Number(result?.probability);
										const safe = Number.isFinite(prob) ? prob : 0;
										return `Xác suất: ${Math.round(safe * 100)}%`;
									})()}
										</p>
									</div>
								</div>
								<div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
									 <div 
									 className={`h-3 rounded-full transition-all duration-1000 progress-bar ${
									 result.decision === 'approve' 
									 ? 'bg-gradient-to-r from-blue-400 to-blue-600' 
									 : 'bg-gradient-to-r from-red-500 to-red-600'
									 }`}
								 data-progress={String(Math.max(0, Math.min(100, Math.round(((Number.isFinite(Number(result?.probability)) ? Number(result?.probability) : 0) * 100)))))}
									 ></div>
								</div>
							</div>

							{/* Credit Health */}
							<div className="space-y-3">
								<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Tình trạng tín dụng</h3>
								{(() => {
									const cs = Number(result?.credit_score);
									const val = Number.isFinite(cs) ? cs / 10 : 0;
									return <CreditHealthBar value={val} label="Credit Health" />;
								})()}
							</div>

							{/* Timeline */}
							{result.trend && result.trend.length > 0 && (
								<div className="space-y-3">
									<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Hành trình duyệt vay</h3>
									<LoanTimeline items={result.trend} />
								</div>
							)}

							{/* Explanation */}
							{explain && Array.isArray(explain.features) && (
								<div className="space-y-3">
									<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Yếu tố ảnh hưởng</h3>
									<div className="space-y-2">
										{explain.features.slice(0, 5).map((f, i) => (
											<div key={i} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
												<span className="text-sm font-medium">{f.name}</span>
												<span className={`text-sm font-bold ${
													typeof f.shap === 'number' && f.shap > 0 
														? 'text-primary' 
														: 'text-red-600'
												}` }>
													{typeof f.shap === 'number' ? f.shap.toFixed(2) : 'N/A'}
												</span>
											</div>
										))}
									</div>
								</div>
							)}

							{/* Recommendations */}
							{recs.length > 0 && (
								<div className="space-y-3">
									<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Khuyến nghị cải thiện</h3>
									<div className="space-y-2">
										{recs.map((r, i) => (
											<div key={i} className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
												<div className="flex items-start gap-2">
													<span className="text-blue-600 text-lg">💡</span>
													<div>
														<p className="text-sm text-gray-800 dark:text-gray-200">{r.message}</p>
														{typeof r.expected_gain === 'number' && (
															<span className="text-xs text-blue-600 font-medium">
																Cải thiện: +{r.expected_gain}%
															</span>
														)}
													</div>
												</div>
											</div>
										))}
									</div>
								</div>
							)}
						</div>
					) : (
						<div className="text-center py-12">
							<div className="icon-wrapper mx-auto mb-4">
								<span className="text-3xl">🔮</span>
							</div>
							<h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-2">
								Chưa có kết quả
							</h3>
							<p className="text-sm text-gray-500 dark:text-gray-500">
								Nhập thông tin hồ sơ và nhấn "Dự đoán ngay" để xem kết quả
							</p>
						</div>
					)}
				</section>
			</div>
		</div>
	);
}


