"use client"

import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { mockStats, mockEmails } from "@/lib/mock-data"
import { Button } from "@/components/ui/button"
import { 
  MailIcon, 
  CheckCircleIcon, 
  ClockIcon, 
  AlertCircleIcon, 
  RefreshCwIcon,
  BarChart3Icon
} from "lucide-react"
import { formatDate } from "@/lib/utils"

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <div className="flex items-center space-x-2">
          <Button>
            <RefreshCwIcon className="mr-2 h-4 w-4" />
            Process Emails
          </Button>
        </div>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mt-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Emails
            </CardTitle>
            <MailIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.totalEmails}</div>
            <p className="text-xs text-muted-foreground">
              Emails received today
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Processed
            </CardTitle>
            <CheckCircleIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.processedEmails}</div>
            <p className="text-xs text-muted-foreground">
              Successfully processed
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Pending
            </CardTitle>
            <ClockIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.pendingEmails + mockStats.processingEmails}</div>
            <p className="text-xs text-muted-foreground">
              Awaiting processing
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Success Rate
            </CardTitle>
            <BarChart3Icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockStats.successRate}%</div>
            <p className="text-xs text-muted-foreground">
              Processing success rate
            </p>
          </CardContent>
        </Card>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-6">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Emails</CardTitle>
            <CardDescription>
              Recently received emails for processing
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockEmails.slice(0, 3).map((email) => (
                <div key={email.id} className="flex items-center">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{email.subject}</p>
                    <p className="text-sm text-muted-foreground">
                      From: {email.sender}
                    </p>
                    <div className="flex items-center pt-2">
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
                      <span className="ml-4 text-xs text-muted-foreground">
                        {formatDate(email.received_at)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Inventory Alerts</CardTitle>
            <CardDescription>
              Items requiring attention
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center">
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">SKU98765 - Economy Parts</p>
                  <p className="text-sm text-muted-foreground">
                    Current stock: 0
                  </p>
                  <div className="flex items-center pt-2">
                    <span className="flex items-center text-sm text-red-500">
                      <AlertCircleIcon className="mr-1 h-4 w-4" />
                      Out of stock
                    </span>
                    <span className="ml-4 text-xs text-muted-foreground">
                      Last updated: {formatDate('2025-02-26T10:15:00Z')}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
