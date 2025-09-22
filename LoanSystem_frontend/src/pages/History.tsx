import { useEffect, useState } from 'react';
import { Api } from '@/services/api';
import type { HistoryItem } from '@/types/index';
import { LineSimple } from '@/components/charts/Charts';

export default function History() {
	const [items, setItems] = useState<HistoryItem[]>([]);

	useEffect(() => {
		Api.getHistory('demo-user').then(setItems);
	}, []);

	return (
		<div className="space-y-6">
			<section className="card-glass">
				<h3 className="h2-title mb-3">Bảng lịch sử dự đoán</h3>
				<div className="overflow-x-auto">
					<table className="min-w-full text-sm">
						<thead>
							<tr className="text-left text-gray-700 dark:text-gray-300">
								<th className="p-2">Ngày</th>
								<th className="p-2">Điểm</th>
								<th className="p-2">Quyết định</th>
							</tr>
						</thead>
						<tbody>
							{items.map((it, i) => (
								<tr key={i} className="border-t border-white/20">
									<td className="p-2">{new Date(it.date).toLocaleString()}</td>
									<td className="p-2">{it.score}</td>
									<td className="p-2">{it.decision.toUpperCase()}</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</section>
			<section className="card-glass">
				<h3 className="h2-title mb-3">Xu hướng điểm theo thời gian</h3>
				<LineSimple data={items.map((x, i) => ({ name: `${i + 1}`, value: x.score / 10 }))} />
			</section>
		</div>
	);
}


