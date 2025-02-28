"use client"

import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { mockEmails } from "@/lib/mock-data"
import { formatDate } from "@/lib/utils"
import { 
  CheckCircleIcon, 
  ClockIcon, 
  AlertCircleIcon, 
  RefreshCwIcon,
  SearchIcon,
  FilterIcon
} from "lucide-react"
import { Input } from "@/components/ui/input"

export default function EmailsPage() {
  return (
    <DashboardLayout>
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Emails</h2>
        <div className="flex items-center space-x-2">
          <Button>
            <RefreshCwIcon className="mr-2 h-4 w-4" />
            Process Emails
          </Button>
        </div>
      </div>
      
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Email Processing</CardTitle>
          <CardDescription>
            View and manage emails for ERP processing
          </CardDescription>
          <div className="flex items-center space-x-2 mt-4">
            <div className="relative flex-1">
              <SearchIcon className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search emails..."
                className="pl-8"
              />
            </div>
            <Button variant="outline" size="sm">
              <FilterIcon className="mr-2 h-4 w-4" />
              Filter
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Subject</TableHead>
                <TableHead>Sender</TableHead>
                <TableHead>Received</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockEmails.map((email) => (
                <TableRow key={email.id}>
                  <TableCell className="font-medium">{email.subject}</TableCell>
                  <TableCell>{email.sender}</TableCell>
                  <TableCell>{formatDate(email.received_at)}</TableCell>
                  <TableCell>
                    {email.processing_status === 'success' && (
                      <span className="flex items-center text-sm text-green-500">
                        <CheckCircleIcon className="mr-1 h-4 w-4" />
                        Processed
                      </span>
                    )}
                    {email.processing_status === 'pending' && (
                      <span className="flex items-center text-sm text-yellow-500">
                        <ClockIcon className="mr-1 h-4 w-4" />
                        Pending
                      </span>
                    )}
                    {email.processing_status === 'processing' && (
                      <span className="flex items-center text-sm text-blue-500">
                        <RefreshCwIcon className="mr-1 h-4 w-4" />
                        Processing
                      </span>
                    )}
                    {email.processing_status === 'failed' && (
                      <span className="flex items-center text-sm text-red-500">
                        <AlertCircleIcon className="mr-1 h-4 w-4" />
                        Failed
                      </span>
                    )}
                  </TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
