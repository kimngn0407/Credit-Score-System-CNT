import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password || !name) {
      setError('Vui lòng nhập đầy đủ thông tin!');
      return;
    }
    // Giả lập đăng ký, thực tế gọi API
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-light/40 to-white dark:from-primary-dark/40 dark:to-gray-900">
      <form className="card-glass w-full max-w-md p-8 space-y-6" onSubmit={handleRegister}>
        <h2 className="text-2xl font-bold text-center mb-4">Đăng ký tài khoản AI Tín dụng</h2>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Họ và tên</label>
          <input className="input-base w-full" type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Nhập họ tên" />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium">Email/SĐT</label>
          <input className="input-base w-full" type="text" value={email} onChange={e => setEmail(e.target.value)} placeholder="Nhập email hoặc số điện thoại" />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium">Mật khẩu</label>
          <input className="input-base w-full" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Nhập mật khẩu" />
        </div>
        <button type="submit" className="btn-primary w-full py-3 text-lg">Đăng ký</button>
        <div className="text-center text-sm mt-2">
          Đã có tài khoản? <a href="/login" className="text-primary hover:underline">Đăng nhập</a>
        </div>
      </form>
    </div>
  );
}
