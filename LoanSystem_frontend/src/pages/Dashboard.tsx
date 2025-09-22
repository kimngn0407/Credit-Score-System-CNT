import { useEffect, useState } from 'react';
import { PieSimple, BarSimple, LineSimple } from '@/components/charts/Charts';
import CustomerMap from '@/components/map/CustomerMap';
import { Api } from '@/services/api';
import { useAuth, Role } from '@/contexts/AuthContext';

export default function Dashboard() {
	const { user } = useAuth();
	const [pie, setPie] = useState<{ name: string; value: number }[]>([]);
	const [bar, setBar] = useState<{ name: string; value: number }[]>([]);
	const [line, setLine] = useState<{ name: string; value: number }[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		Api.getDashboardSummary().then((d: any) => {
			setPie(d.pie);
			setBar(d.bar);
			setLine(d.line);
			setLoading(false);
		});
	}, []);

	// Role-based data and configurations
	const getRoleConfig = (role: Role) => {
		const configs = {
			USER: {
				title: 'Bảng điều khiển Khách hàng',
				subtitle: 'Theo dõi hồ sơ vay và tình trạng tín dụng của bạn',
				stats: [
					{ label: 'Hồ sơ của tôi', value: '3', icon: '📋', color: 'from-blue-500 to-blue-600' },
					{ label: 'Đã duyệt', value: '2', icon: '✅', color: 'from-emerald-500 to-emerald-600' },
					{ label: 'Đang chờ', value: '1', icon: '⏳', color: 'from-yellow-500 to-yellow-600' },
					{ label: 'Tỷ lệ thành công', value: '66.7%', icon: '📊', color: 'from-purple-500 to-purple-600' },
				],
				quickActions: [
					{ label: 'Tạo hồ sơ mới', icon: '📝', color: 'emerald', description: 'Đăng ký khoản vay mới' },
					{ label: 'Xem lịch sử', icon: '📈', color: 'blue', description: 'Lịch sử giao dịch' },
					{ label: 'Hỗ trợ', icon: '💬', color: 'purple', description: 'Liên hệ hỗ trợ' },
				]
			},
			STAFF: {
				title: 'Bảng điều khiển Nhân viên',
				subtitle: 'Quản lý hồ sơ vay và hỗ trợ khách hàng',
				stats: [
					{ label: 'Hồ sơ chờ xử lý', value: '45', icon: '📋', color: 'from-blue-500 to-blue-600' },
					{ label: 'Đã xử lý hôm nay', value: '23', icon: '✅', color: 'from-emerald-500 to-emerald-600' },
					{ label: 'Cần xem xét', value: '12', icon: '⚠️', color: 'from-red-500 to-red-600' },
					{ label: 'Hiệu suất', value: '85%', icon: '📊', color: 'from-purple-500 to-purple-600' },
				],
				quickActions: [
					{ label: 'Xử lý hồ sơ', icon: '⚡', color: 'emerald', description: 'Duyệt hồ sơ mới' },
					{ label: 'Báo cáo', icon: '📊', color: 'blue', description: 'Báo cáo hiệu suất' },
					{ label: 'Khách hàng', icon: '👥', color: 'purple', description: 'Quản lý khách hàng' },
				]
			},
			ADMIN: {
				title: 'Bảng điều khiển Quản trị',
				subtitle: 'Tổng quan hệ thống và quản lý toàn bộ hoạt động',
				stats: [
					{ label: 'Tổng hồ sơ', value: '1,234', icon: '📋', color: 'from-blue-500 to-blue-600' },
					{ label: 'Đã duyệt', value: '856', icon: '✅', color: 'from-emerald-500 to-emerald-600' },
					{ label: 'Từ chối', value: '378', icon: '❌', color: 'from-red-500 to-red-600' },
					{ label: 'Tỷ lệ duyệt', value: '69.4%', icon: '📊', color: 'from-purple-500 to-purple-600' },
				],
				quickActions: [
					{ label: 'Quản lý hệ thống', icon: '⚙️', color: 'emerald', description: 'Cấu hình hệ thống' },
					{ label: 'Báo cáo tổng hợp', icon: '📊', color: 'blue', description: 'Báo cáo toàn diện' },
					{ label: 'Quản lý người dùng', icon: '👥', color: 'purple', description: 'Phân quyền người dùng' },
				]
			}
		};
		return configs[role] || configs.USER;
	};

	const roleConfig = getRoleConfig(user?.role || 'USER');

	if (loading) {
		return (
			<div className="space-y-6">
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
					{Array.from({ length: 4 }).map((_, i) => (
						<div key={i} className="stat-card animate-pulse">
							<div className="h-8 bg-gray-300 rounded mb-2"></div>
							<div className="h-4 bg-gray-300 rounded w-2/3 mx-auto"></div>
						</div>
					))}
				</div>
				<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
					{Array.from({ length: 4 }).map((_, i) => (
						<div key={i} className="card-glass animate-pulse">
							<div className="h-6 bg-gray-300 rounded mb-4"></div>
							<div className="h-64 bg-gray-300 rounded"></div>
						</div>
					))}
				</div>
			</div>
		);
	}

	return (
		<div className="space-y-8">
			{/* Role-based Welcome Section */}
			<div className="text-center py-8">
				<div className="flex items-center justify-center gap-3 mb-4">
					<div className={`icon-wrapper ${
						user?.role === 'USER' ? 'bg-gradient-to-br from-blue-500 to-blue-600' :
						user?.role === 'STAFF' ? 'bg-gradient-to-br from-emerald-500 to-emerald-600' :
						'bg-gradient-to-br from-purple-500 to-purple-600'
					}`}>
						<span className="text-2xl">
							{user?.role === 'USER' ? '👤' : user?.role === 'STAFF' ? '👨‍💼' : '👑'}
						</span>
					</div>
					<div className="text-left">
						<h1 className="text-4xl font-bold gradient-text">{roleConfig.title}</h1>
						<div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
							<span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded-full font-medium">
								{user?.role}
							</span>
							<span>•</span>
							<span>Xin chào, {user?.username || 'Khách'}</span>
						</div>
					</div>
				</div>
				<p className="text-gray-600 dark:text-gray-400 text-lg">{roleConfig.subtitle}</p>
			</div>

			{/* Role-based Stats Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				{roleConfig.stats.map((stat, index) => (
					<div key={stat.label} className="stat-card group hover:scale-105 transition-transform duration-300">
						<div className={`icon-wrapper mx-auto mb-4 bg-gradient-to-br ${stat.color} group-hover:scale-110 transition-transform duration-300`}>
							<span className="text-2xl">{stat.icon}</span>
						</div>
						<div className="stat-value">{stat.value}</div>
						<div className="stat-label">{stat.label}</div>
					</div>
				))}
			</div>

			{/* Charts Grid */}
			<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
				<div className="xl:col-span-2 space-y-6">
					{/* Approval/Rejection Ratio */}
					<section className="card-glass group">
						<div className="flex items-center gap-3 mb-6">
							<div className="icon-wrapper">
								<span className="text-xl">🥧</span>
							</div>
							<div>
								<h3 className="h2-title mb-0">Tỷ lệ duyệt / từ chối</h3>
								<p className="text-sm text-gray-600 dark:text-gray-400">Phân bố quyết định tín dụng</p>
							</div>
						</div>
						<div className="h-80">
							<PieSimple data={pie as any} />
						</div>
					</section>

					{/* Factors Analysis */}
					<section className="card-glass group">
						<div className="flex items-center gap-3 mb-6">
							<div className="icon-wrapper">
								<span className="text-xl">📊</span>
							</div>
							<div>
								<h3 className="h2-title mb-0">Yếu tố ảnh hưởng</h3>
								<p className="text-sm text-gray-600 dark:text-gray-400">Các yếu tố quan trọng trong quyết định</p>
							</div>
						</div>
						<div className="h-80">
							<BarSimple data={bar} />
						</div>
					</section>

					{/* Trend Analysis */}
					<section className="card-glass group">
						<div className="flex items-center gap-3 mb-6">
							<div className="icon-wrapper">
								<span className="text-xl">📈</span>
							</div>
							<div>
								<h3 className="h2-title mb-0">Xu hướng xác suất duyệt</h3>
								<p className="text-sm text-gray-600 dark:text-gray-400">Biến động theo thời gian</p>
							</div>
						</div>
						<div className="h-80">
							<LineSimple data={line} />
						</div>
					</section>
				</div>

				{/* Customer Map */}
				<section className="xl:col-span-1 card-glass group">
					<div className="flex items-center gap-3 mb-6">
						<div className="icon-wrapper">
							<span className="text-xl">🗺️</span>
						</div>
						<div>
							<h3 className="h2-title mb-0">Bản đồ khách hàng</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">Phân bố địa lý</p>
						</div>
					</div>
					<div className="h-96 rounded-xl overflow-hidden">
						<CustomerMap />
					</div>
				</section>
			</div>

			{/* Role-based Quick Actions */}
			<div className="card-glass">
				<h3 className="h2-title mb-6">Thao tác nhanh</h3>
				<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
					{roleConfig.quickActions.map((action, index) => (
						<button 
							key={action.label}
							className={`p-4 rounded-xl border transition-colors group hover:scale-105 ${
								action.color === 'emerald' ? 'border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 hover:bg-emerald-100 dark:hover:bg-emerald-900/30' :
								action.color === 'blue' ? 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30' :
								'border-purple-200 dark:border-purple-800 bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30'
							}`}
						>
							<div className="flex items-center gap-3">
								<div className={`icon-wrapper ${
									action.color === 'emerald' ? 'bg-gradient-to-br from-emerald-500 to-emerald-600' :
									action.color === 'blue' ? 'bg-gradient-to-br from-blue-500 to-blue-600' :
									'bg-gradient-to-br from-purple-500 to-purple-600'
								}`}>
									<span className="text-lg">{action.icon}</span>
								</div>
								<div className="text-left">
									<div className={`font-semibold ${
										action.color === 'emerald' ? 'text-emerald-700 dark:text-emerald-300' :
										action.color === 'blue' ? 'text-blue-700 dark:text-blue-300' :
										'text-purple-700 dark:text-purple-300'
									}`}>
										{action.label}
									</div>
									<div className={`text-sm ${
										action.color === 'emerald' ? 'text-emerald-600 dark:text-emerald-400' :
										action.color === 'blue' ? 'text-blue-600 dark:text-blue-400' :
										'text-purple-600 dark:text-purple-400'
									}`}>
										{action.description}
									</div>
								</div>
							</div>
						</button>
					))}
				</div>
			</div>
		</div>
	);
}


