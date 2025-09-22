import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const { loginAs } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('USER');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    // Giả lập xác thực, thực tế gọi API
    if (!email || !password) {
      setError('Vui lòng nhập đầy đủ thông tin!');
      return;
    }
    // Chỉ USER được đăng ký trực tiếp, STAFF/ADMIN do quản trị cấp
  loginAs({ email, role: role as 'USER' | 'STAFF' | 'ADMIN' });
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-light/40 to-white dark:from-primary-dark/40 dark:to-gray-900">
      <form className="card-glass w-full max-w-md p-8 space-y-6" onSubmit={handleLogin}>
        <h2 className="text-2xl font-bold text-center mb-4">Đăng nhập hệ thống AI Tín dụng</h2>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Email/SĐT</label>
          <input className="input-base w-full" type="text" value={email} onChange={e => setEmail(e.target.value)} placeholder="Nhập email hoặc số điện thoại" />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium">Mật khẩu</label>
          <input className="input-base w-full" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Nhập mật khẩu" />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium">Vai trò</label>
          <select className="input-base w-full" value={role} onChange={e => setRole(e.target.value as 'USER' | 'STAFF' | 'ADMIN')} title="Chọn vai trò đăng nhập">
            <option value="USER">Người dùng</option>
            <option value="STAFF">Nhân viên tín dụng</option>
            <option value="ADMIN">Quản trị viên</option>
          </select>
        </div>
        <button type="submit" className="btn-primary w-full py-3 text-lg">Đăng nhập</button>
        <div className="text-center text-sm mt-2">
          Chưa có tài khoản? <a href="/register" className="text-primary hover:underline">Đăng ký ngay</a>
        </div>
      </form>
    </div>
  );
}
