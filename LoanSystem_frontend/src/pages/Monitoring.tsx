import { useEffect, useState } from 'react';
import { Api } from '@/services/api';
import type { MonitoringMetrics } from '../types';
import { LineSimple, BarSimple } from '@/components/charts/Charts';
import RoleWelcome from '@/components/RoleWelcome';
import { useAuth } from '@/contexts/AuthContext';

export default function Monitoring() {
	const { user } = useAuth();
	const [metrics, setMetrics] = useState<MonitoringMetrics>({});
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		Api.getMonitoringMetrics().then(data => {
			setMetrics(data);
			setLoading(false);
		});
	}, []);

	// Mock data for demonstration
	const systemStats = [
		{ label: 'Tổng yêu cầu hôm nay', value: '1,234', icon: '📊', color: 'from-blue-400 to-blue-500' },
		{ label: 'Thời gian phản hồi TB', value: '245ms', icon: '⚡', color: 'from-primary to-primary-dark' },
		{ label: 'Tỷ lệ thành công', value: '99.2%', icon: '✅', color: 'from-primary-light to-primary' },
		{ label: 'Lỗi hệ thống', value: '3', icon: 'from-red-400 to-red-600' },
	];

	if (loading) {
		return (
			<div className="space-y-6">
				<RoleWelcome />
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
					{Array.from({ length: 4 }).map((_, i) => (
						<div key={i} className="stat-card animate-pulse">
							<div className="h-8 bg-gray-300 rounded mb-2"></div>
							<div className="h-4 bg-gray-300 rounded w-2/3 mx-auto"></div>
						</div>
					))}
				</div>
			</div>
		);
	}

	return (
		<div className="space-y-8">
			{/* Role-based Welcome */}
			<RoleWelcome />

			{/* Header */}
			<div className="text-center py-8">
				<h1 className="text-4xl font-bold gradient-text mb-4">Giám sát Hệ thống</h1>
				<p className="text-gray-600 dark:text-gray-400 text-lg">
					{user?.role === 'STAFF' 
						? 'Theo dõi hiệu suất xử lý hồ sơ và hỗ trợ khách hàng'
						: 'Giám sát toàn diện hệ thống AI và hiệu suất hoạt động'
					}
				</p>
			</div>

			{/* System Stats */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				{systemStats.map((stat, index) => (
					<div key={stat.label} className="stat-card group hover:scale-105 transition-transform duration-300">
						<div className={`icon-wrapper mx-auto mb-4 bg-gradient-to-br ${stat.color} group-hover:scale-110 transition-transform duration-300`}>
							<span className="text-2xl">{stat.icon}</span>
						</div>
						<div className="stat-value">{stat.value}</div>
						<div className="stat-label">{stat.label}</div>
					</div>
				))}
			</div>

			{/* Monitoring Charts */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<section className="card-glass group">
					<div className="flex items-center gap-3 mb-6">
						<div className="icon-wrapper">
							<span className="text-xl">⚡</span>
						</div>
						<div>
							<h3 className="h2-title mb-0">API Latency</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">Thời gian phản hồi API (ms)</p>
						</div>
					</div>
					<div className="h-64 flex items-center justify-center">
						<div className="text-center">
							<div className="text-3xl font-bold text-emerald-600 mb-2">
								{metrics.apiLatencyMs?.slice(-1)[0] || '245'}ms
							</div>
							<div className="text-sm text-gray-600 dark:text-gray-400">
								Trung bình 10 yêu cầu gần nhất
							</div>
						</div>
					</div>
				</section>

				<section className="card-glass group">
					<div className="flex items-center gap-3 mb-6">
						<div className="icon-wrapper">
							<span className="text-xl">📈</span>
						</div>
						<div>
							<h3 className="h2-title mb-0">Độ chính xác theo thời gian</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">Xu hướng hiệu suất AI</p>
						</div>
					</div>
					<div className="h-64">
						<LineSimple data={metrics.accuracyOverTime ?? [
							{ name: 'T2', value: 85 },
							{ name: 'T3', value: 87 },
							{ name: 'T4', value: 89 },
							{ name: 'T5', value: 91 },
							{ name: 'T6', value: 88 },
							{ name: 'T7', value: 93 },
							{ name: 'CN', value: 90 }
						]} />
					</div>
				</section>
			</div>

			{/* Additional Monitoring for Admin */}
			{user?.role === 'ADMIN' && (
				<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
					<section className="card-glass group">
						<div className="flex items-center gap-3 mb-6">
							<div className="icon-wrapper">
								<span className="text-xl">👥</span>
							</div>
							<div>
								<h3 className="h2-title mb-0">Hoạt động người dùng</h3>
								<p className="text-sm text-gray-600 dark:text-gray-400">Thống kê theo vai trò</p>
							</div>
						</div>
						<div className="h-64">
							<BarSimple data={[
								{ name: 'USER', value: 156 },
								{ name: 'STAFF', value: 23 },
								{ name: 'ADMIN', value: 3 }
							]} />
						</div>
					</section>

					<section className="card-glass group">
						<div className="flex items-center gap-3 mb-6">
							<div className="icon-wrapper">
								<span className="text-xl">🔧</span>
							</div>
							<div>
								<h3 className="h2-title mb-0">Trạng thái hệ thống</h3>
								<p className="text-sm text-gray-600 dark:text-gray-400">Các thành phần chính</p>
							</div>
						</div>
						<div className="space-y-3">
							{[
								{ name: 'API Gateway', status: 'healthy', color: 'emerald' },
								{ name: 'AI Model', status: 'healthy', color: 'emerald' },
								{ name: 'Database', status: 'warning', color: 'yellow' },
								{ name: 'Cache', status: 'healthy', color: 'emerald' }
							].map((service, index) => (
								<div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
									<span className="font-medium">{service.name}</span>
									<span className={`px-2 py-1 rounded-full text-xs font-medium ${
										service.color === 'emerald' 
											? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-400'
											: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
									}`}>
										{service.status}
									</span>
								</div>
							))}
						</div>
					</section>
				</div>
			)}
		</div>
	);
}


