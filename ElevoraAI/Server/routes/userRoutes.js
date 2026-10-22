import express from "express";
const router = express.Router();

import {
  registerUser,
  verifySignupOtp,
  loginUser,
  currentStreak,
  logout,
  feedback,
  googleUser,
  latestNews,
  updateProfile,
  getProfile,
  changePassword,
  forgotPassword,
  resetPassword,
} from "../controller/userController.js";
import { authenticateToken } from "../middleware/authMiddleware.js";
import { passwordChangeLimiter } from "../utils/passwordChangeLimiter.js";

router.post("/auth/signup", registerUser);
router.post("/auth/verify-otp", verifySignupOtp);
router.post("/auth/login", loginUser);
// Logout must NOT require a valid token: an expired session (the exact case
// that leaves a stale cookie behind) would otherwise be rejected by the
// middleware before the handler can clear the cookie.
router.get("/logout", logout);
router.put("/update-profile", authenticateToken, updateProfile);
router.get("/get-profile", authenticateToken, getProfile);
router.post("/auth/google", googleUser);
router.post("/feedback", authenticateToken, feedback);
router.get("/user/streak", authenticateToken, currentStreak);
router.post(
  "/change-password",
  authenticateToken,
  passwordChangeLimiter,
  changePassword
);
router.post("/auth/forgot-password", forgotPassword);
router.post("/auth/reset-password/:resetToken", resetPassword);

router.get("/latest-news",latestNews)



export default router;
