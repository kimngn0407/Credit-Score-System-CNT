
import { NavLink, Link, useLocation } from 'react-router-dom';
import { useAuth, Role } from '@/contexts/AuthContext';
import { useTheme } from '@/contexts/ThemeContext';
import clsx from 'clsx';

interface SidebarProps {
	isOpen: boolean;
	onClose: () => void;
	collapsed: boolean;
	onToggleCollapse: () => void;
}

export default function Sidebar({ isOpen, onClose, collapsed, onToggleCollapse }: SidebarProps) {
	const location = useLocation();
	const { user, loginAs, logout } = useAuth();
	const { theme, toggle } = useTheme();

	const navItems = [
		{ to: '/dashboard', label: 'Trang chủ', icon: '📊', roles: ['USER', 'STAFF', 'ADMIN'] },
		{ to: '/predict', label: 'Dự đoán', icon: '🔮', roles: ['USER', 'STAFF', 'ADMIN'] },
		{ to: '/what-if', label: 'Kịch bản', icon: '🎯', roles: ['USER', 'STAFF', 'ADMIN'] },
		{ to: '/risk', label: 'Phân tích rủi ro', icon: '⚠️', roles: ['USER', 'STAFF', 'ADMIN'] },
		{ to: '/history', label: 'Lịch sử', icon: '📈', roles: ['USER', 'STAFF', 'ADMIN'] },
		{ to: '/monitoring', label: 'Giám sát', icon: '👁️', roles: ['STAFF', 'ADMIN'] },
	];

	const navLink = ({ isActive }: { isActive: boolean }) =>
		clsx(
			'relative flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300 group overflow-hidden',
			'text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary-light',
			'hover:bg-gradient-to-r hover:from-primary/10 hover:to-primary-light/20 dark:hover:from-primary-dark/20 dark:hover:to-primary/20',
			'hover:shadow-lg hover:scale-[1.03] hover:-translate-y-0.5',
			{
				'bg-gradient-to-r from-primary-light to-primary dark:from-primary-dark/40 dark:to-primary/40 text-primary-dark dark:text-primary-light shadow-lg scale-[1.03] -translate-y-0.5': isActive,
			}
		);

	const filteredNavItems = navItems.filter(item => 
		!user || item.roles.includes(user.role)
	);

		if (location.pathname === '/login' || location.pathname === '/register') {
			return (
				<div className="fixed top-0 left-0 z-50 h-20 w-full bg-gradient-to-r from-primary-light to-primary-dark flex items-center justify-center shadow-xl">
					<div className="flex items-center gap-4">
						<div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center text-white shadow-lg">
							<span className="text-2xl font-bold">AI</span>
						</div>
						<span className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">AI Tín Dụng</span>
					</div>
				</div>
			);
		}

		return (
			<>
				{/* Mobile Overlay */}
				{isOpen && (
					<div 
						className="fixed inset-0 bg-black/50 z-40 lg:hidden"
						onClick={onClose}
					/>
				)}
				{/* Sidebar */}
				<div className={clsx(
					'fixed top-0 left-0 z-50 h-full bg-gradient-to-b from-primary-light/30 to-white dark:from-primary-dark/40 dark:to-gray-800',
					'border-r border-primary/30 dark:border-primary-dark/30 shadow-2xl backdrop-blur-xl',
					'transition-all duration-300 ease-in-out',
					collapsed ? 'w-16' : 'w-64',
					isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
				)}>
					{/* Header */}
					<div className="relative p-4 border-b border-gray-200/50 dark:border-gray-700/50">
						{/* Background Pattern */}
						<div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-primary-dark/10"></div>
						<div className="relative flex items-center justify-between">
							{!collapsed && (
								<Link to="/" className="flex items-center gap-3 group">
									<div className="relative">
										<div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center text-white shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-105">
											<span className="text-lg font-bold">AI</span>
										</div>
										<div className="absolute -inset-1 bg-gradient-to-r from-primary-light to-primary-dark rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-300"></div>
									</div>
									<div>
										<span className="text-lg font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
											AI Tín Dụng
										</span>
										<p className="text-xs text-gray-500 dark:text-gray-400 font-medium">Smart Credit</p>
									</div>
								</Link>
							)}
						</div>
					</div>
					{/* Collapse Button */}
					<button
						onClick={onToggleCollapse}
						className="flex items-center justify-center w-8 h-8 rounded-xl bg-gray-100 dark:bg-gray-800 hover:bg-emerald-100 dark:hover:bg-emerald-900/30 text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-all duration-300 hover:scale-110"
					>
						<span className="text-sm font-bold">{collapsed ? '→' : '←'}</span>
					</button>
					{/* User Profile */}
					{user && (
						<div className="p-4 border-b border-gray-200/50 dark:border-gray-700/50">
							<div className={clsx(
								'relative flex items-center gap-3 p-3 rounded-2xl overflow-hidden group',
								collapsed ? 'justify-center' : 'bg-gradient-to-r from-gray-50/80 to-gray-100/80 dark:from-gray-800/80 dark:to-gray-700/80 backdrop-blur-sm'
							)}>
								{/* Background Pattern */}
								{!collapsed && (
									<div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 via-transparent to-blue-500/5"></div>
								)}
								<div className={`relative w-10 h-10 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-105 ${
									user && user.role === 'USER' ? 'bg-gradient-to-br from-blue-500 to-blue-600' :
									user && user.role === 'STAFF' ? 'bg-gradient-to-br from-emerald-500 to-emerald-600' :
									'bg-gradient-to-br from-purple-500 to-purple-600'
								}`}>
									<span className="text-lg">
										{user && user.role === 'USER' ? '👤' : user && user.role === 'STAFF' ? '👨‍💼' : '👑'}
									</span>
								</div>
								{!collapsed && (
									<div className="relative flex-1 min-w-0">
										<div className="text-sm font-bold text-gray-900 dark:text-white truncate">
											{user && user.username}
										</div>
										<div className="text-xs text-gray-500 dark:text-gray-400 font-medium">
											{user && user.role}
										</div>
									</div>
								)}
							</div>
						</div>
					)}
					{/* Navigation */}
					<nav className="flex-1 p-4 space-y-1">
						{filteredNavItems.map((item) => (
							<NavLink
								key={item.to}
								to={item.to}
								className={navLink}
								onClick={() => {
									// Close mobile menu when navigating
									if (window.innerWidth < 1024) {
										onClose();
									}
								}}
							>
								{/* Background Pattern */}
								<div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-transparent to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
								<div className="relative w-8 h-8 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 flex items-center justify-center group-hover:from-emerald-100 group-hover:to-emerald-200 dark:group-hover:from-emerald-800 dark:group-hover:to-emerald-700 transition-all duration-300 group-hover:scale-110">
									<span className="text-lg">{item.icon}</span>
								</div>
								{!collapsed && (
									<span className="relative font-semibold text-sm">{item.label}</span>
								)}
							</NavLink>
						))}
					</nav>
					{/* Controls Section */}
					<div className="p-4 border-t border-gray-200/50 dark:border-gray-700/50 space-y-2">
						{/* Theme Toggle */}
						<button
							onClick={toggle}
							className={clsx(
								'relative w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300 group overflow-hidden',
								'text-gray-700 dark:text-gray-300 hover:text-emerald-600 dark:hover:text-emerald-400',
								'hover:bg-gradient-to-r hover:from-emerald-50 hover:to-emerald-100 dark:hover:from-emerald-900/20 dark:hover:to-emerald-800/20',
								'hover:shadow-lg hover:scale-[1.02] hover:-translate-y-0.5',
								collapsed && 'justify-center'
							)}
						>
							{/* Background Pattern */}
							<div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-transparent to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
							<div className="relative w-8 h-8 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 flex items-center justify-center group-hover:from-emerald-100 group-hover:to-emerald-200 dark:group-hover:from-emerald-800 dark:group-hover:to-emerald-700 transition-all duration-300 group-hover:scale-110">
								<span className="text-lg">
									{theme === 'light' ? '🌙' : '☀️'}
								</span>
							</div>
							{!collapsed && (
								<span className="relative font-semibold text-sm">
									{theme === 'light' ? 'Dark Mode' : 'Light Mode'}
								</span>
							)}
						</button>
						{/* Role Switcher */}
						{!collapsed && (
							<div className="space-y-3">
								<div className="text-xs font-bold text-gray-500 dark:text-gray-400 px-2 uppercase tracking-wider">
									Vai trò
								</div>
								<div className="grid grid-cols-3 gap-2">
									{(['USER', 'STAFF', 'ADMIN'] as Role[]).map(r => (
										<button
											key={r}
											onClick={() => loginAs({ email: `demo+${r.toLowerCase()}@mail.com`, role: r })}
											className={clsx(
												'relative px-3 py-2 text-xs font-bold rounded-xl border-2 transition-all duration-300 flex flex-col items-center gap-1 group overflow-hidden',
												{
													'bg-gradient-to-br from-emerald-100 to-emerald-200 text-emerald-700 border-emerald-300 dark:from-emerald-900/40 dark:to-emerald-800/40 dark:text-emerald-300 dark:border-emerald-600 shadow-lg scale-105': user && user.role === r,
													'bg-gradient-to-br from-gray-100 to-gray-200 text-gray-600 border-gray-300 hover:from-emerald-50 hover:to-emerald-100 hover:text-emerald-600 hover:border-emerald-300 dark:from-gray-800 dark:to-gray-700 dark:text-gray-400 dark:border-gray-600 dark:hover:from-emerald-900/20 dark:hover:to-emerald-800/20 dark:hover:text-emerald-400 dark:hover:border-emerald-600 hover:scale-105 hover:shadow-md': !user || user.role !== r,
												}
											)}
										>
											<span className="text-sm">
												{r === 'USER' ? '👤' : r === 'STAFF' ? '👨‍💼' : '👑'}
											</span>
											<span className="font-bold">{r}</span>
										</button>
									))}
								</div>
							</div>
						)}
						{/* Logout Button */}
						{user && (
							<button
								onClick={logout}
								className={clsx(
									'relative w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300 group overflow-hidden',
									'text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300',
									'hover:bg-gradient-to-r hover:from-red-50 hover:to-red-100 dark:hover:from-red-900/20 dark:hover:to-red-800/20',
									'hover:shadow-lg hover:scale-[1.02] hover:-translate-y-0.5',
									collapsed && 'justify-center'
								)}
							>
								{/* Background Pattern */}
								<div className="absolute inset-0 bg-gradient-to-r from-red-500/5 via-transparent to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
								<div className="relative w-8 h-8 rounded-xl bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center group-hover:from-red-600 group-hover:to-red-700 transition-all duration-300 group-hover:scale-110 shadow-lg">
									<span className="text-lg">🚪</span>
								</div>
								{!collapsed && (
									<span className="relative font-semibold text-sm">Logout</span>
								)}
							</button>
						)}
					</div>
					{/* Footer */}
					<div className="p-4 border-t border-gray-200/50 dark:border-gray-700/50">
						{!collapsed && (
							<div className="text-center">
								<div className="text-xs font-bold text-gray-400 dark:text-gray-500 mb-1">
									AI Tín Dụng
								</div>
								<div className="text-xs text-gray-400 dark:text-gray-600">
									v1.0
								</div>
							</div>
						)}
					</div>
				</div>
			</>
		);
}
