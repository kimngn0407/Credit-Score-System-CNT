import { useAuth, Role } from '@/contexts/AuthContext';

interface RoleWelcomeProps {
	className?: string;
}

export default function RoleWelcome({ className = '' }: RoleWelcomeProps) {
	const { user } = useAuth();

	const getRoleInfo = (role: Role) => {
		const roleInfo = {
			USER: {
				icon: '👤',
				title: 'Khách hàng',
				description: 'Quản lý hồ sơ vay và theo dõi tình trạng tín dụng',
				color: 'from-blue-500 to-blue-600',
				features: [
					'Tạo và theo dõi hồ sơ vay',
					'Xem lịch sử giao dịch',
					'Nhận thông báo cập nhật',
					'Truy cập công cụ dự đoán AI'
				]
			},
			STAFF: {
				icon: '👨‍💼',
				title: 'Nhân viên',
				description: 'Xử lý hồ sơ vay và hỗ trợ khách hàng',
				color: 'from-emerald-500 to-emerald-600',
				features: [
					'Duyệt và xử lý hồ sơ vay',
					'Quản lý danh sách khách hàng',
					'Tạo báo cáo hiệu suất',
					'Hỗ trợ khách hàng trực tiếp'
				]
			},
			ADMIN: {
				icon: '👑',
				title: 'Quản trị viên',
				description: 'Quản lý toàn bộ hệ thống và phân quyền',
				color: 'from-purple-500 to-purple-600',
				features: [
					'Quản lý người dùng và phân quyền',
					'Cấu hình hệ thống AI',
					'Xem báo cáo tổng hợp',
					'Giám sát hoạt động hệ thống'
				]
			}
		};
		return roleInfo[role] || roleInfo.USER;
	};

	if (!user) {
		return (
			<div className={`card-glass text-center py-8 ${className}`}>
				<div className="icon-wrapper mx-auto mb-4 bg-gradient-to-br from-gray-500 to-gray-600">
					<span className="text-2xl">🔐</span>
				</div>
				<h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
					Chào mừng đến với AI Tín Dụng
				</h2>
				<p className="text-gray-600 dark:text-gray-400 mb-4">
					Vui lòng chọn vai trò để bắt đầu sử dụng hệ thống
				</p>
				<div className="flex justify-center gap-2">
					{(['USER', 'STAFF', 'ADMIN'] as Role[]).map(role => (
						<span key={role} className="px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-sm font-medium">
							{role}
						</span>
					))}
				</div>
			</div>
		);
	}

	const roleInfo = getRoleInfo(user.role);

	return (
		<div className={`card-glass ${className}`}>
			<div className="flex items-start gap-4">
				<div className={`icon-wrapper bg-gradient-to-br ${roleInfo.color}`}>
					<span className="text-2xl">{roleInfo.icon}</span>
				</div>
				<div className="flex-1">
					<div className="flex items-center gap-2 mb-2">
						<h2 className="text-xl font-bold text-gray-800 dark:text-gray-200">
							Xin chào, {user.username}
						</h2>
						<span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-xs font-medium text-gray-600 dark:text-gray-400">
							{user.role}
						</span>
					</div>
					<p className="text-gray-600 dark:text-gray-400 mb-4">
						{roleInfo.description}
					</p>
					<div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
						{roleInfo.features.map((feature, index) => (
							<div key={index} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
								<span className="text-emerald-500">✓</span>
								<span>{feature}</span>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	);
}
