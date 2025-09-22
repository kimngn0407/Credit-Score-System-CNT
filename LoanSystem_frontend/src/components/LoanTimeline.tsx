type Item = {
	date: string;
	score: number;
	decision: 'approve' | 'reject' | 'pending';
};

export default function LoanTimeline({ items }: { items: Item[] }) {
	return (
		<ol className="relative border-s border-gray-200 dark:border-gray-800 ps-4">
			{items.map((it, idx) => (
				<li key={idx} className="mb-6 ms-6">
					<span
						className="absolute -start-3 flex h-6 w-6 items-center justify-center rounded-full ring-8 ring-white dark:ring-gray-900"
						style={{
							backgroundColor:
								it.decision === 'approve' ? '#22c55e' : it.decision === 'pending' ? '#eab308' : '#ef4444',
						}}
					/>
					<div className="flex items-center justify-between text-sm">
						<time className="text-gray-500">{new Date(it.date).toLocaleDateString()}</time>
						<span className="font-medium">Score: {it.score}</span>
					</div>
					<p className="text-sm">
						{it.decision === 'approve' ? 'Được duyệt 🎉' : it.decision === 'pending' ? 'Đang cải thiện ✅' : 'Bị từ chối ❌'}
					</p>
				</li>
			))}
		</ol>
	);
}


