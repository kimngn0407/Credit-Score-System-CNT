import { useEffect, useState } from 'react';
import clsx from 'clsx';

type Props = {
	value: number; // 0..1 or 0..100 if > 1
	label?: string;
};

export default function CreditHealthBar({ value, label }: Props) {
	const normalized = value > 1 ? value / 100 : value;
	const [progress, setProgress] = useState(0);

	useEffect(() => {
		const target = Math.max(0, Math.min(1, normalized));
		const id = requestAnimationFrame(() => setProgress(target));
		return () => cancelAnimationFrame(id);
	}, [normalized]);

	const pct = Math.round(progress * 100);
	const color = progress < 0.4 ? 'bg-red-500' : progress < 0.7 ? 'bg-yellow-500' : 'bg-green-500';

	return (
		<div className="w-full">
			<div className="flex items-center justify-between mb-1 text-sm">
				<span>{label ?? 'Credit Health'}</span>
				<span className="tabular-nums font-semibold">{pct}%</span>
			</div>
			<div className="h-3 w-full rounded bg-gray-200 dark:bg-gray-800 overflow-hidden">
				<div
					className={clsx('h-full transition-all duration-700 ease-out', color)}
					style={{ width: `${pct}%` }}
				/>
			</div>
		</div>
	);
}


