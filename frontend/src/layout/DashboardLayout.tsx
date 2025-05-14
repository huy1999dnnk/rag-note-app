import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { Outlet } from 'react-router';
import { AppSidebar } from '@/components/dashboard/sidebar/app-side-bar';
import { DropdownMenuTheme } from '@/components/theme/theme-select';
import ChatbotModal from '@/components/chatbot/chatbot-modal';
import { useTitle } from '@/hooks/useTitle';
export default function DashboardLayout() {
  useTitle('Dashboard');
  return (
    <SidebarProvider>
      <div className="flex h-screen w-full">
        <AppSidebar />
        <main className="flex-1 flex flex-col overflow-hidden w-full">
          <div className="w-full p-2 flex gap-3 items-center">
            <SidebarTrigger />
            <DropdownMenuTheme />
          </div>
          <div className="flex-1 h-full min-h-0 w-full p-2">
            <Outlet />
          </div>
        </main>
        <ChatbotModal />
      </div>
    </SidebarProvider>
  );
}
