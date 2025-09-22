import { Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider, RequireRole } from '@/contexts/AuthContext';
import Login from '@/pages/Login';
import Register from '@/pages/Register';
import RequireAuth from '@/contexts/RequireAuth';
import Layout from '@/components/layout/Layout';
import Dashboard from '@/pages/Dashboard';
import Predict from '@/pages/Predict';
import Risk from '@/pages/Risk';
import WhatIf from '@/pages/WhatIf';
import History from '@/pages/History';
import Monitoring from '@/pages/Monitoring';

export default function App() {
	return (
		<ThemeProvider>
			<AuthProvider>
				<Routes>
					<Route path="/login" element={<Layout><div className="container-app py-6"><Login /></div></Layout>} />
					<Route path="/register" element={<Layout><div className="container-app py-6"><Register /></div></Layout>} />
					<Route path="/*" element={<RequireAuth><Layout><div className="container-app py-6">
						<Routes>
							<Route path="/dashboard" element={<Dashboard />} />
							<Route path="/predict" element={<Predict />} />
							<Route path="/risk" element={<Risk />} />
							<Route path="/what-if" element={<WhatIf />} />
							<Route path="/history" element={<History />} />
							<Route path="/monitoring" element={<RequireRole roles={["STAFF", "ADMIN"]}><Monitoring /></RequireRole>} />
						</Routes>
					</div></Layout></RequireAuth>} />
				</Routes>
			</AuthProvider>
		</ThemeProvider>
	);
}


