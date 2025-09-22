import {
	PieChart,
	Pie,
	Cell,
	ResponsiveContainer,
	BarChart,
	Bar,
	XAxis,
	YAxis,
	Tooltip,
	LineChart,
	Line,
	RadarChart,
	PolarGrid,
	PolarAngleAxis,
	PolarRadiusAxis,
	Radar,
	Legend,
	CartesianGrid,
} from 'recharts';

const COLORS = {
	primary: ['#10b981', '#22c55e', '#84cc16'],
	secondary: ['#3b82f6', '#8b5cf6', '#f59e0b'],
	status: ['#10b981', '#ef4444', '#f59e0b', '#8b5cf6'],
	gradient: {
		emerald: ['#10b981', '#22c55e', '#84cc16'],
		blue: ['#3b82f6', '#6366f1', '#8b5cf6'],
		red: ['#ef4444', '#f97316', '#f59e0b'],
	},
};

const CustomTooltip = ({ active, payload, label }: any) => {
	if (active && payload && payload.length) {
		return (
			<div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
				<p className="font-semibold text-gray-900 dark:text-white">{label}</p>
				{payload.map((entry: any, index: number) => (
					<p key={index} className="text-sm" style={{ color: entry.color }}>
						{entry.name}: {entry.value}
					</p>
				))}
			</div>
		);
	}
	return null;
};

export function PieSimple({ data }: { data: { name: string; value: number; color?: string }[] }) {
	return (
		<ResponsiveContainer width="100%" height={280}>
			<PieChart>
				<Pie 
					data={data} 
					dataKey="value" 
					nameKey="name" 
					outerRadius={100}
					innerRadius={40}
					paddingAngle={2}
					strokeWidth={2}
					stroke="rgba(255,255,255,0.8)"
				>
					{data.map((entry, index) => (
						<Cell 
							key={`cell-${index}`} 
							fill={entry.color ?? COLORS.primary[index % COLORS.primary.length]}
							stroke="rgba(255,255,255,0.8)"
							strokeWidth={2}
						/>
					))}
				</Pie>
				<Tooltip content={<CustomTooltip />} />
				<Legend 
					verticalAlign="bottom" 
					height={36}
					iconType="circle"
					wrapperStyle={{ fontSize: '14px' }}
				/>
			</PieChart>
		</ResponsiveContainer>
	);
}

export function BarSimple({ data }: { data: { name: string; value: number }[] }) {
	return (
		<ResponsiveContainer width="100%" height={280}>
			<BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
				<CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
				<XAxis 
					dataKey="name" 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<YAxis 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<Tooltip content={<CustomTooltip />} />
				<Bar 
					dataKey="value" 
					fill="url(#barGradient)"
					radius={[4, 4, 0, 0]}
					stroke="rgba(255,255,255,0.8)"
					strokeWidth={1}
				>
					<defs>
						<linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
							<stop offset="0%" stopColor="#3b82f6" />
							<stop offset="100%" stopColor="#1d4ed8" />
						</linearGradient>
					</defs>
				</Bar>
			</BarChart>
		</ResponsiveContainer>
	);
}

export function LineSimple({ data }: { data: { name: string; value: number }[] }) {
	return (
		<ResponsiveContainer width="100%" height={280}>
			<LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
				<CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
				<XAxis 
					dataKey="name" 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<YAxis 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<Tooltip content={<CustomTooltip />} />
				<Line 
					type="monotone" 
					dataKey="value" 
					stroke="url(#lineGradient)"
					strokeWidth={3}
					dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
					activeDot={{ r: 6, stroke: '#10b981', strokeWidth: 2, fill: 'white' }}
				>
					<defs>
						<linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
							<stop offset="0%" stopColor="#10b981" />
							<stop offset="50%" stopColor="#22c55e" />
							<stop offset="100%" stopColor="#84cc16" />
						</linearGradient>
					</defs>
				</Line>
			</LineChart>
		</ResponsiveContainer>
	);
}

export function RadarSimple({ data }: { data: { subject: string; A: number; B: number }[] }) {
	return (
		<ResponsiveContainer width="100%" height={320}>
			<RadarChart cx="50%" cy="50%" outerRadius="80%" data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
				<PolarGrid stroke="rgba(0,0,0,0.1)" />
				<PolarAngleAxis 
					dataKey="subject" 
					tick={{ fontSize: 12 }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<PolarRadiusAxis 
					tick={{ fontSize: 10 }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<Tooltip content={<CustomTooltip />} />
				<Radar 
					name="Hiện tại" 
					dataKey="A" 
					stroke="#ef4444" 
					fill="#ef4444" 
					fillOpacity={0.3}
					strokeWidth={2}
				/>
				<Radar 
					name="Lý tưởng" 
					dataKey="B" 
					stroke="#22c55e" 
					fill="#22c55e" 
					fillOpacity={0.3}
					strokeWidth={2}
				/>
				<Legend />
			</RadarChart>
		</ResponsiveContainer>
	);
}

// New enhanced chart components
export function DonutChart({ data, title }: { data: { name: string; value: number; color?: string }[]; title?: string }) {
	const total = data.reduce((sum, item) => sum + item.value, 0);
	
	return (
		<div className="w-full h-full">
			{title && (
				<h3 className="text-lg font-semibold text-center mb-4 text-gray-800 dark:text-gray-200">
					{title}
				</h3>
			)}
			<ResponsiveContainer width="100%" height={280}>
				<PieChart>
					<Pie 
						data={data} 
						dataKey="value" 
						nameKey="name" 
						outerRadius={100}
						innerRadius={60}
						paddingAngle={2}
						strokeWidth={2}
						stroke="rgba(255,255,255,0.8)"
					>
						{data.map((entry, index) => (
							<Cell 
								key={`cell-${index}`} 
								fill={entry.color ?? COLORS.primary[index % COLORS.primary.length]}
								stroke="rgba(255,255,255,0.8)"
								strokeWidth={2}
							/>
						))}
					</Pie>
					<Tooltip content={<CustomTooltip />} />
					<text 
						x="50%" 
						y="50%" 
						textAnchor="middle" 
						dominantBaseline="middle" 
						className="text-2xl font-bold fill-gray-700 dark:fill-gray-300"
					>
						{total}
					</text>
				</PieChart>
			</ResponsiveContainer>
		</div>
	);
}

export function AreaChart({ data, dataKey, name }: { data: any[]; dataKey: string; name: string }) {
	return (
		<ResponsiveContainer width="100%" height={280}>
			<LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
				<defs>
					<linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stopColor="#10b981" stopOpacity={0.8} />
						<stop offset="100%" stopColor="#10b981" stopOpacity={0.1} />
					</linearGradient>
				</defs>
				<CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
				<XAxis 
					dataKey="name" 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<YAxis 
					tick={{ fontSize: 12 }}
					axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
					tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
				/>
				<Tooltip content={<CustomTooltip />} />
				<Line 
					type="monotone" 
					dataKey={dataKey} 
					stroke="#10b981"
					strokeWidth={3}
					fill="url(#areaGradient)"
					dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
					activeDot={{ r: 6, stroke: '#10b981', strokeWidth: 2, fill: 'white' }}
				/>
			</LineChart>
		</ResponsiveContainer>
	);
}


