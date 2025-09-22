import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';

type Theme = 'light' | 'dark';

type ThemeContextValue = {
	theme: Theme;
	setTheme: (theme: Theme) => void;
		toggle: () => void;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export const ThemeProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
	const [theme, setThemeState] = useState<Theme>(() => {
		const saved = localStorage.getItem('theme') as Theme | null;
		return saved ?? 'light';
	});

	useEffect(() => {
		localStorage.setItem('theme', theme);
		const root = document.documentElement;
		if (theme === 'dark') root.classList.add('dark');
		else root.classList.remove('dark');
	}, [theme]);

	const setTheme = (t: Theme) => setThemeState(t);
	const toggle = () => setThemeState(prev => (prev === 'light' ? 'dark' : 'light'));

	const value = useMemo(() => ({ theme, setTheme, toggle }), [theme]);
	return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

export const useTheme = () => {
	const ctx = useContext(ThemeContext);
	if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
	return ctx;
};


