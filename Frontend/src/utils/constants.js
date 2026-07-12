// ======================================================
// USER ROLES
// ======================================================

export const ROLES = Object.freeze({
  ADMIN: "ADMIN",
  ASSET_MANAGER: "ASSET_MANAGER",
  DEPARTMENT_HEAD: "DEPARTMENT_HEAD",
  EMPLOYEE: "EMPLOYEE",
});

// ======================================================
// DEPARTMENTS
// ======================================================

export const DEPARTMENT_STATUS = Object.freeze({
  ACTIVE: "ACTIVE",
  INACTIVE: "INACTIVE",
});

// ======================================================
// ASSETS
// ======================================================

export const ASSET_STATUS = Object.freeze({
  AVAILABLE: "AVAILABLE",
  ALLOCATED: "ALLOCATED",
  RESERVED: "RESERVED",
  UNDER_MAINTENANCE: "UNDER_MAINTENANCE",
  LOST: "LOST",
  RETIRED: "RETIRED",
  DISPOSED: "DISPOSED",
});

export const CONDITION = Object.freeze({
  NEW: "NEW",
  GOOD: "GOOD",
  FAIR: "FAIR",
  POOR: "POOR",
  DAMAGED: "DAMAGED",
});

// ======================================================
// ALLOCATIONS
// ======================================================

export const ALLOCATION_STATUS = Object.freeze({
  ACTIVE: "ACTIVE",
  RETURNED: "RETURNED",
});

export const TRANSFER_STATUS = Object.freeze({
  REQUESTED: "REQUESTED",
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
  COMPLETED: "COMPLETED",
});

// ======================================================
// BOOKINGS
// ======================================================

export const BOOKING_STATUS = Object.freeze({
  UPCOMING: "UPCOMING",
  ONGOING: "ONGOING",
  COMPLETED: "COMPLETED",
  CANCELLED: "CANCELLED",
});

// ======================================================
// MAINTENANCE
// ======================================================

export const MAINTENANCE_STATUS = Object.freeze({
  PENDING: "PENDING",
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
  TECHNICIAN_ASSIGNED: "TECHNICIAN_ASSIGNED",
  IN_PROGRESS: "IN_PROGRESS",
  RESOLVED: "RESOLVED",
});

export const PRIORITY = Object.freeze({
  LOW: "LOW",
  MEDIUM: "MEDIUM",
  HIGH: "HIGH",
  CRITICAL: "CRITICAL",
});

// ======================================================
// AUDITS
// ======================================================

export const AUDIT_ITEM_RESULT = Object.freeze({
  UNVERIFIED: "UNVERIFIED",
  VERIFIED: "VERIFIED",
  MISSING: "MISSING",
  DAMAGED: "DAMAGED",
});

export const AUDIT_CYCLE_STATUS = Object.freeze({
  OPEN: "OPEN",
  CLOSED: "CLOSED",
});

// ======================================================
// NOTIFICATIONS
// ======================================================

export const NOTIFICATION_TYPE = Object.freeze({
  ALERT: "ALERT",
  APPROVAL: "APPROVAL",
  BOOKING: "BOOKING",
});