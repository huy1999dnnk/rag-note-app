import { Outlet } from 'react-router';
import { DropdownMenuTheme } from '@/components/theme/theme-select';
export default function AuthLayout() {
  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <div className="mb-4 flex items-center justify-center">
          <DropdownMenuTheme />
        </div>
        <Outlet />
      </div>
    </div>
  );
}
