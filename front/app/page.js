"use client";

import { Container, Typography } from "@mui/material";
import { DashboardLayout } from "@toolpad/core";
import Upload from "./components/upload";


function SidebarFooterAccount() {
  return (
    <Container sx={{border: '1px solid green', padding: '10px', textAlign: 'center'}}>
      Hola
    </Container>
  )
}


export default function Home() {
  return (
    <DashboardLayout
      slots={{
        toolbarAccount: () => null, sidebarFooter: SidebarFooterAccount
      }}
    >
      <Upload />
    </DashboardLayout>
  );
}
