import express from "express";
import { scanResumeATS } from "../controller/atsController.js";

const router = express.Router();

/**
 * ATS Resume Scanner Routes
 */

/**
 * @route   POST /api/v1/ats/scan
 * @desc    Analyze resume for ATS compatibility
 * @access  Public
 */
router.post("/scan", scanResumeATS);

export default router;
