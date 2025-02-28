"use client"

import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { mockInventory } from "@/lib/mock-data"
import { formatDate } from "@/lib/utils"
import { 
  SearchIcon,
  FilterIcon,
  PlusIcon,
  AlertCircleIcon
} from "lucide-react"
import { Input } from "@/components/ui/input"

export default function InventoryPage() {
  return (
    <DashboardLayout>
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Inventory</h2>
        <div className="flex items-center space-x-2">
          <Button>
            <PlusIcon className="mr-2 h-4 w-4" />
            Add Item
          </Button>
        </div>
      </div>
      
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Inventory Management</CardTitle>
          <CardDescription>
            View and manage your inventory items
          </CardDescription>
          <div className="flex items-center space-x-2 mt-4">
            <div className="relative flex-1">
              <SearchIcon className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search inventory..."
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
                <TableHead>SKU</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Last Updated</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockInventory.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">{item.sku}</TableCell>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>
                    {item.quantity === 0 ? (
                      <span className="flex items-center text-sm text-red-500">
                        <AlertCircleIcon className="mr-1 h-4 w-4" />
                        Out of stock
                      </span>
                    ) : item.quantity < 100 ? (
                      <span className="flex items-center text-sm text-yellow-500">
                        {item.quantity} - Low stock
                      </span>
                    ) : (
                      <span>{item.quantity}</span>
                    )}
                  </TableCell>
                  <TableCell>${item.unit_price.toFixed(2)}</TableCell>
                  <TableCell>{item.category}</TableCell>
                  <TableCell>{formatDate(item.last_updated)}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">
                      Edit
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
