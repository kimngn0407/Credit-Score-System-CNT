import { ReactNode } from 'react';
import { useAuth, Role } from '@/contexts/AuthContext';

interface RoleBasedContentProps {
	allowedRoles: Role[];
	children: ReactNode;
	fallback?: ReactNode;
	className?: string;
}

export default function RoleBasedContent({ 
	allowedRoles, 
	children, 
	fallback,
	className = '' 
}: RoleBasedContentProps) {
	const { user } = useAuth();

	if (!user) {
		return (
			<div className={`card-glass text-center py-8 ${className}`}>
				<div className="icon-wrapper mx-auto mb-4 bg-gradient-to-br from-gray-500 to-gray-600">
					<span className="text-2xl">🔐</span>
				</div>
				<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
					Yêu cầu đăng nhập
				</h3>
				<p className="text-gray-600 dark:text-gray-400">
					Vui lòng đăng nhập để truy cập nội dung này
				</p>
			</div>
		);
	}

	if (!allowedRoles.includes(user.role)) {
		return fallback || (
			<div className={`card-glass text-center py-8 ${className}`}>
				<div className="icon-wrapper mx-auto mb-4 bg-gradient-to-br from-red-500 to-red-600">
					<span className="text-2xl">🚫</span>
				</div>
				<h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
					Không có quyền truy cập
				</h3>
				<p className="text-gray-600 dark:text-gray-400 mb-4">
					Bạn cần quyền {allowedRoles.join(' hoặc ')} để truy cập nội dung này
				</p>
				<div className="flex justify-center gap-2">
					{allowedRoles.map(role => (
						<span key={role} className="px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-sm font-medium">
							{role}
						</span>
					))}
				</div>
			</div>
		);
	}

	return <>{children}</>;
}

// Convenience components for specific roles
export function UserOnly({ children, fallback, className }: Omit<RoleBasedContentProps, 'allowedRoles'>) {
	return (
		<RoleBasedContent allowedRoles={['USER']} fallback={fallback} className={className}>
			{children}
		</RoleBasedContent>
	);
}

export function StaffOnly({ children, fallback, className }: Omit<RoleBasedContentProps, 'allowedRoles'>) {
	return (
		<RoleBasedContent allowedRoles={['STAFF']} fallback={fallback} className={className}>
			{children}
		</RoleBasedContent>
	);
}

export function AdminOnly({ children, fallback, className }: Omit<RoleBasedContentProps, 'allowedRoles'>) {
	return (
		<RoleBasedContent allowedRoles={['ADMIN']} fallback={fallback} className={className}>
			{children}
		</RoleBasedContent>
	);
}

export function StaffAndAdmin({ children, fallback, className }: Omit<RoleBasedContentProps, 'allowedRoles'>) {
	return (
		<RoleBasedContent allowedRoles={['STAFF', 'ADMIN']} fallback={fallback} className={className}>
			{children}
		</RoleBasedContent>
	);
}
