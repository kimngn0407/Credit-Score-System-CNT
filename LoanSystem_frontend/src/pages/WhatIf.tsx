import { useState } from 'react';
import { LineSimple } from '@/components/charts/Charts';

export default function WhatIf() {
	const [income, setIncome] = useState(625); // 625 USD
	const [loan, setLoan] = useState(2083); // 2083 USD

	// Placeholder: vẽ đường xu hướng theo input tạm thời
	const data = Array.from({ length: 6 }).map((_, i) => ({
		name: `${i}`,
		value: Math.max(10, Math.min(95, 50 + (income / 100) * 2 - (loan / 1000) * 5 + i * 3)),
	}));

	return (
		<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<section className="card-glass space-y-4">
				<h2 className="h2-title">Giả lập kịch bản</h2>
				<label className="flex items-center gap-3 text-sm">
					<span className="label-sm">Thu nhập</span>
					<input className="input-base w-full" type="number" value={income}
						onChange={e => setIncome(Number(e.target.value))} />
				</label>
				<label className="flex items-center gap-3 text-sm">
					<span className="label-sm">Khoản vay</span>
					<input className="input-base w-full" type="number" value={loan}
						onChange={e => setLoan(Number(e.target.value))} />
				</label>
				<p className="text-xs text-gray-600 dark:text-gray-400">Phần API what-if sẽ gọi nhiều lần predict để lấy chuỗi kết quả.</p>
			</section>
			<section className="card-glass">
				<h3 className="h2-title mb-3">Xu hướng khả năng duyệt khi thay đổi biến</h3>
				<LineSimple data={data} />
			</section>
		</div>
	);
}


