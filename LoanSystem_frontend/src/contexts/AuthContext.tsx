import React, { createContext, useContext, useMemo, useState } from 'react';
import * as Api from '../services/api';

export type Role = 'USER' | 'STAFF' | 'ADMIN';

type User = {
	id: number; // Changed from string to number to match backend Long
	username: string;
	role: Role;
	fullName?: string;
	email?: string;
};

type AuthContextValue = {
	user: User | null;
	login: (username: string, password: string) => Promise<void>;
	register: (userData: { username: string; password: string; fullName?: string; email?: string; role?: Role }) => Promise<void>;
	loginAs: (user: { email: string; role: Role }) => void; // Keep for demo purposes
	logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
	const [user, setUser] = useState<User | null>(null);

	const login = async (username: string, password: string) => {
		try {
			const userDto = await Api.login(username, password);
			setUser({
				id: userDto.id!,
				username: userDto.username!,
				role: userDto.role as Role,
				fullName: userDto.fullName,
				email: userDto.email
			});
		} catch (error) {
			console.error('Login failed:', error);
			throw error;
		}
	};

	const register = async (userData: { username: string; password: string; fullName?: string; email?: string; role?: Role }) => {
		try {
			const userDto = await Api.register({
				username: userData.username,
				passwordHash: userData.password,
				fullName: userData.fullName,
				email: userData.email,
				role: userData.role || 'USER',
				themePreference: 'light'
			});
			setUser({
				id: userDto.id!,
				username: userDto.username!,
				role: userDto.role as Role,
				fullName: userDto.fullName,
				email: userDto.email
			});
		} catch (error) {
			console.error('Registration failed:', error);
			throw error;
		}
	};

    const loginAs = (userInfo: { email: string; role: Role }) => {
        // Demo function - use numeric ID to avoid NaN errors
        setUser({ id: 1, username: userInfo.email, role: userInfo.role });
    };

	const logout = () => setUser(null);

	const value = useMemo(() => ({ user, login, register, loginAs, logout }), [user]);
	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
	const ctx = useContext(AuthContext);
	if (!ctx) throw new Error('useAuth must be used within AuthProvider');
	return ctx;
};

export const RequireRole: React.FC<React.PropsWithChildren<{ roles: Role[] }>> = ({ roles, children }) => {
	const { user } = useAuth();
	if (!user) return <div className="text-center">Hãy đăng nhập (demo chọn role ở navbar)</div>;
	if (!roles.includes(user.role)) return <div className="text-center">Bạn không có quyền truy cập</div>;
	return <>{children}</>;
};


