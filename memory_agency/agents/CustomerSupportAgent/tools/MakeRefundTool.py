from typing import Optional

from agency_swarm.tools import BaseTool
from pydantic import Field

NON_REFUNDABLE = ["dairy", "perishable", "fresh produce", "meat", "fish"]


class MakeRefundTool(BaseTool):
    """Process refund requests."""

    order_id: str = Field(..., description="Order ID to refund")
    item_description: str = Field(..., description="Item being refunded")
    reason: Optional[str] = Field(None, description="Reason for refund")

    def run(self) -> str:
        """Process refund and store result."""
        # Check if item is refundable
        if any(item in self.item_description.lower() for item in NON_REFUNDABLE):
            msg = f"Cannot refund {self.item_description} - non-refundable item"
            raise ValueError(msg)

        # Process refund
        msg = f"Refund processed for order {self.order_id}"
        if self.reason:
            msg += f" (Reason: {self.reason})"
        return msg


if __name__ == "__main__":
    # Test non-refundable
    try:
        tool = MakeRefundTool(
            order_id="12345",
            item_description="dairy products - milk",
            reason="Changed mind",
        )
        print(tool.run())
    except ValueError as e:
        print(f"Expected error: {e}")

    # Test refundable
    tool = MakeRefundTool(
        order_id="12345", item_description="T-shirt", reason="Wrong size"
    )
    print(tool.run())
