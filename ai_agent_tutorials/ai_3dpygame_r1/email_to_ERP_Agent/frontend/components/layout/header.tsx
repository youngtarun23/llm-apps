import Link from "next/link";
import { Button } from "@/components/ui/button";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold text-xl">Email to ERP Agent</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link href="/dashboard" className="transition-colors hover:text-foreground/80">
              Dashboard
            </Link>
            <Link href="/emails" className="transition-colors hover:text-foreground/80">
              Emails
            </Link>
            <Link href="/inventory" className="transition-colors hover:text-foreground/80">
              Inventory
            </Link>
            <Link href="/settings" className="transition-colors hover:text-foreground/80">
              Settings
            </Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <nav className="flex items-center">
            <Button variant="ghost" size="sm">
              Sign out
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}
