import { Routes, Route } from "react-router-dom";
import HomePage from "@pages/HomePage/HomePage.js";
import SignInPage from "@pages/SignInPage/SignInPage.js";
import SignUpPage from "@pages/SignUpPage/SignUpPage.js";
import DashboardPage from "@pages/DashboardPage/DashboardPage.js";
import DocumentDetailPage from "@pages/DocumentDetailsPage/DocumentDetails.js";
import UploadDocumentsPage from "@pages/UploadDocumentsPage/UploadDocumentsPage.js";


const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/sign-in" element={<SignInPage />} />
      <Route path="/sign-up" element={<SignUpPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/documents/:id" element={<DocumentDetailPage />} />
        <Route path="/upload" element={<UploadDocumentsPage/>}/>
    </Routes>
  );
};

export default AppRouter;
