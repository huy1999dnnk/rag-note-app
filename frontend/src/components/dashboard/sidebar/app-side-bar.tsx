import { Settings } from 'lucide-react';

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { Link } from 'react-router';
import { NavUser } from '@/components/dashboard/sidebar/nav-user';
import SpaceTree from '@/components/dashboard/sidebar/space-tree';
import AddNewWorkspace from './add-new-workspace';
// Menu items.
const items = [
  {
    title: 'Settings',
    url: 'setting',
    icon: Settings,
  },
];

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent className="flex justify-between">
            <SidebarGroupLabel>Space</SidebarGroupLabel>
            <SidebarGroupLabel>
              <AddNewWorkspace>
                <SidebarMenuButton>
                  <div className="cursor-pointer hover:bg-accent">
                    <span className="text-sm">Add New Workspace</span>
                  </div>
                </SidebarMenuButton>
              </AddNewWorkspace>
            </SidebarGroupLabel>
          </SidebarGroupContent>
          <SidebarGroupContent>
            <SidebarGroup>
              <SidebarGroupContent>
                <SpaceTree />
              </SidebarGroupContent>
            </SidebarGroup>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <Link
                      to={{
                        pathname: item.url,
                      }}
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <NavUser />
      </SidebarFooter>
    </Sidebar>
  );
}
