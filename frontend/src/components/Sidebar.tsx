"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpenIcon, HomeIcon, AcademicCapIcon, ChartBarIcon } from "@heroicons/react/24/outline";

const navigation = [
  { name: "ホーム", href: "/home", icon: HomeIcon },
  { name: "教材", href: "/materials", icon: BookOpenIcon },
  { name: "演習", href: "/exercises", icon: AcademicCapIcon },
  { name: "ダッシュボード", href: "/dashboard", icon: ChartBarIcon },
];

interface SidebarProps {
  isCollapsed?: boolean;
}

export default function Sidebar({ isCollapsed = false }: SidebarProps) {
  const pathname = usePathname();

  return (
    <div className={`flex h-full flex-col bg-gradient-to-b from-gray-900 to-gray-800 transition-all duration-300 ${isCollapsed ? "w-20" : "w-64"}`}>
      <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
        <div className="flex flex-shrink-0 items-center px-4">
          <h1 className={`font-bold text-white transition-all duration-300 ${isCollapsed ? "text-sm" : "text-xl"}`}>
            {isCollapsed ? "学習" : "学習アプリ"}
          </h1>
        </div>
        <nav className="mt-8 flex-1 space-y-1 px-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`
                  group flex items-center px-2 py-3 text-sm font-medium rounded-xl transition-all
                  ${isActive ? "bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg" : "text-gray-300 hover:bg-gray-700 hover:text-white"}
                  ${isCollapsed ? "justify-center" : ""}
                `}
                title={isCollapsed ? item.name : undefined}
              >
                <item.icon
                  className={`
                    h-6 w-6 flex-shrink-0 transition-all
                    ${isActive ? "text-white" : "text-gray-400 group-hover:text-white"}
                    ${isCollapsed ? "" : "mr-3"}
                  `}
                  aria-hidden="true"
                />
                {!isCollapsed && <span>{item.name}</span>}
              </Link>
            );
          })}
        </nav>

      </div>
    </div>
  );
}
