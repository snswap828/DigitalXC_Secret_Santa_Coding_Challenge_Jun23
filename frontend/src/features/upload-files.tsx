
"use client";

import { Button } from "@/components/ui/button";

import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import z from "zod";
import { toast } from "sonner";
import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";
import { ItbaleData, ResponseError } from "@/lib/types";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { apiClient } from "@/api/api";
import { useState } from "react";
import * as XLSX from 'xlsx';



export default function UploadFiles() {
    const [tableData, setTableData] = useState<ItbaleData[]>([]);
    const FileFormSchema = z
        .object({
            files: z.instanceof(File, {
                message: "Please select a file to upload"
            }).refine(
                (file) => file && file.size <= 10 * 1024 * 1024,
                { message: "File size must be less than 10MB" }
            ).refine(
                (file) => file && ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'].includes(file.type),
                { message: "Only Excel (.xlsx) files are supported" }
            ),
            previous: z.instanceof(File, {
                message: "Please select a previous assignment file to upload"
            }).refine(
                (file) => file && file.size <= 10 * 1024 * 1024,
                { message: "File size must be less than 10MB" }
            ).refine(
                (file) => file && ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'].includes(file.type),
                { message: "Only Excel (.xlsx) files are supported" }
            ),
        });

    type FileFormValues = z.infer<typeof FileFormSchema>;

    const form = useForm<FileFormValues>({
        resolver: zodResolver(FileFormSchema),
        defaultValues: {
            files: null as unknown as File, // Initialize with null or empty file
        },
    });




    // Upload single file
    const uploadFileMutation = useMutation({
        mutationFn: async (file: File) => {
            const formData = new FormData();
            formData.append('employee', file);
            const previousFile = form.getValues('previous');
            if (previousFile) {
                formData.append('previous', previousFile);
            }
            // Update status to uploading
            const response = await apiClient.post(
                `assign`,
                formData,
            );
            return { success: response.status === 200, data: response.data };
        },
        onSuccess(data) {
            setTableData(data.data.data as ItbaleData[]);
            toast.success(`uploaded successfully!`);
        },
        onError: (error: AxiosError<ResponseError>, file: File) => {
            // Update status to error
            const errorMessage =
                error.response?.data?.message ||
                'Something went wrong, please try again';
            toast.error(`Error uploading ${file.name}`, {
                description: errorMessage,
            });
        },
    });


    const handleDownload = () => {
        // Create workbook
        const worksheet = XLSX.utils.json_to_sheet(tableData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Secret Santa");
        // Generate and download file
        const currentYear = new Date().getFullYear();
        XLSX.writeFile(workbook, `Secret-Santa-Game-Result-${currentYear}.xlsx`);
    };



    return (
        <div className="space-y-4">
            <h2 className="text-2xl font-bold">Upload File</h2>
            <p className="text-sm text-gray-500">
                Upload your Excel file to assign Secret Santa.
            </p>
            <p className="text-sm text-gray-500">
                Please ensure the file is in .xlsx format and does not exceed 10MB.
            </p>

            <Card className="p-6">
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit((data: FileFormValues) =>
                            uploadFileMutation.mutate(data.files),
                        )}
                        className="space-y-4"
                    >
                        <FormField
                            control={form.control}
                            name="files"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel className="text-sm font-medium">
                                        Upload New File
                                    </FormLabel>
                                    <FormControl>
                                        <div className="space-y-3">
                                            <div className="flex items-center gap-4">

                                                <div className="flex-1">
                                                    <Input
                                                        type="file"
                                                        onChange={(e) => {
                                                            const file = e.target.files?.[0];
                                                            field.onChange(file);
                                                        }}
                                                        className="cursor-pointer"
                                                        accept=".xlsx"
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </FormControl>
                                    <p className="text-xs text-gray-500 mt-1">Supported formats: xlsx</p>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="previous"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel className="text-sm font-medium">
                                        Upload Previos Year File
                                    </FormLabel>
                                    <FormControl>
                                        <div className="space-y-3">
                                            <div className="flex items-center gap-4">

                                                <div className="flex-1">
                                                    <Input
                                                        type="file"
                                                        onChange={(e) => {
                                                            const file = e.target.files?.[0];
                                                            field.onChange(file);
                                                        }}
                                                        className="cursor-pointer"
                                                        accept=".xlsx"
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </FormControl>
                                    <p className="text-xs text-gray-500 mt-1">Supported formats: xlsx</p>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button type="submit" disabled={uploadFileMutation.isPending}>
                            {uploadFileMutation.isPending ? 'Generating Assignments...' : 'Generate Assignments'}
                        </Button>
                    </form>
                </Form>
            </Card>

            <Card className="p-6 mt-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold">Uploaded Data</h3>
                    {tableData.length > 0 && (
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleDownload}
                        >
                            Download as Excel
                        </Button>
                    )}
                </div>
                {tableData.length > 0 ? (
                    <table className="min-w-full border-collapse">
                        <thead>
                            <tr>
                                <th className="border px-4 py-2">Employee Email</th>
                                <th className="border px-4 py-2">Employee Name</th>
                                <th className="border px-4 py-2">Secret Child Email</th>
                                <th className="border px-4 py-2">Secret Child Name</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.map((row, index) => (
                                <tr key={index}>
                                    <td className="border px-4 py-2">{row.Employee_EmailID}</td>
                                    <td className="border px-4 py-2">{row.Employee_Name}</td>
                                    <td className="border px-4 py-2">{row.Secret_Child_EmailID}</td>
                                    <td className="border px-4 py-2">{row.Secret_Child_Name}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p className="text-gray-500">No data uploaded yet.</p>
                )}
            </Card>
        </div>
    );
}

