import { RadarSimple, BarSimple } from '@/components/charts/Charts';

const radarData = [
	{ subject: 'Thu nhập', A: 50, B: 80 },
	{ subject: 'Khoản vay', A: 40, B: 70 },
	{ subject: 'Lịch sử', A: 35, B: 85 },
	{ subject: 'Nợ xấu', A: 20, B: 90 },
	{ subject: 'Việc làm', A: 60, B: 80 },
];

const barData = [
	{ name: 'Thu nhập thấp', value: 25 },
	{ name: 'Nợ xấu', value: 18 },
	{ name: 'Khoản vay lớn', value: 14 },
];

export default function Risk() {
	return (
		<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<section className="card-glass">
				<h3 className="h2-title mb-3">Radar: Hồ sơ hiện tại vs lý tưởng</h3>
				<RadarSimple data={radarData} />
			</section>
			<section className="card-glass">
				<h3 className="h2-title mb-3">Độ ảnh hưởng các yếu tố</h3>
				<BarSimple data={barData} />
			</section>
		</div>
	);
}


