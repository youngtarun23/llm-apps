"use client"

import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@radix-ui/react-label"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
      </div>
      
      <Tabs defaultValue="email" className="mt-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="email">Email Integration</TabsTrigger>
          <TabsTrigger value="erp">ERP Integration</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>
        
        <TabsContent value="email" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Email Configuration</CardTitle>
              <CardDescription>
                Configure your email integration settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email-address">Email Address</Label>
                <Input
                  id="email-address"
                  placeholder="orders@yourcompany.com"
                  defaultValue="orders@yourcompany.com"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="labels">Gmail Labels to Monitor</Label>
                <Input
                  id="labels"
                  placeholder="Orders, Suppliers"
                  defaultValue="Orders, Suppliers"
                />
                <p className="text-sm text-muted-foreground">
                  Comma-separated list of Gmail labels to monitor
                </p>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="polling-interval">Polling Interval (seconds)</Label>
                <Input
                  id="polling-interval"
                  type="number"
                  placeholder="300"
                  defaultValue="300"
                />
                <p className="text-sm text-muted-foreground">
                  How often to check for new emails (in seconds)
                </p>
              </div>
              
              <div className="flex items-center space-x-2">
                <Switch id="email-active" defaultChecked />
                <Label htmlFor="email-active">Active</Label>
              </div>
              
              <div className="mt-6">
                <Button className="mr-2">
                  Connect Gmail Account
                </Button>
                <Button variant="outline">
                  Test Connection
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="erp" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>ERP Integration</CardTitle>
              <CardDescription>
                Configure your ERP system integration
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="erp-type">ERP System</Label>
                <select 
                  id="erp-type"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="sap">SAP</option>
                  <option value="oracle">Oracle</option>
                  <option value="netsuite">NetSuite</option>
                  <option value="custom">Custom API</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="api-url">API URL</Label>
                <Input
                  id="api-url"
                  placeholder="https://erp-api.example.com/v1"
                  defaultValue="https://erp-api.example.com/v1"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="api-key">API Key</Label>
                <Input
                  id="api-key"
                  type="password"
                  placeholder="Your API key"
                  defaultValue="••••••••••••••••"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <Switch id="erp-active" defaultChecked />
                <Label htmlFor="erp-active">Active</Label>
              </div>
              
              <div className="mt-6">
                <Button className="mr-2">
                  Save Configuration
                </Button>
                <Button variant="outline">
                  Test Connection
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="notifications" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Notification Settings</CardTitle>
              <CardDescription>
                Configure how you receive notifications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="email-notifications">Email Notifications</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive email notifications for important events
                  </p>
                </div>
                <Switch id="email-notifications" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="inventory-alerts">Inventory Alerts</Label>
                  <p className="text-sm text-muted-foreground">
                    Get notified when inventory levels are low
                  </p>
                </div>
                <Switch id="inventory-alerts" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="processing-errors">Processing Errors</Label>
                  <p className="text-sm text-muted-foreground">
                    Get notified when email processing fails
                  </p>
                </div>
                <Switch id="processing-errors" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="daily-summary">Daily Summary</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive a daily summary of processing activity
                  </p>
                </div>
                <Switch id="daily-summary" />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Notification Settings</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </DashboardLayout>
  )
}
