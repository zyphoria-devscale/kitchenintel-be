import json
from typing import Any, Dict, List, Union

from rest_framework import serializers

from .models import Dashboard, Graph


class GraphSerializer(serializers.ModelSerializer):
    """Serializer for Graph model"""

    chart_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Graph
        exclude = ["raw_data", "dashboard"]
        read_only_fields = ["created_at"]

    def get_chart_data(self, obj) -> List[Dict[str, Any]]:
        """Transform raw_data into a format suitable for Recharts.
        
        Args:
            obj: The Graph model instance
            
        Returns:
            A list of dictionaries formatted for Recharts, either as time-series or categorical data
        """
        if not obj.raw_data:
            return []

        try:
            # Parse raw_data if it's a string
            data_dict = self._parse_raw_data(obj.raw_data)
            if not data_dict:
                return []
                
            # Transform to array of objects format for Recharts
            chart_data = self._transform_to_chart_data(data_dict)
            
            # Sort by timestamp if it's time-series data
            if chart_data and "timestamp" in chart_data[0]:
                chart_data.sort(key=lambda x: x["timestamp"])

            return chart_data
        except (json.JSONDecodeError, ValueError, AttributeError) as e:
            # Log error and return empty array if there's an error parsing the data
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing raw_data for graph {obj.id}: {e}")
            return []
    
    def _parse_raw_data(self, raw_data) -> Dict:
        """Parse raw_data into a dictionary."""
        if isinstance(raw_data, str):
            return json.loads(raw_data)
        return raw_data
    
    def _transform_to_chart_data(self, data_dict) -> List[Dict[str, Any]]:
        """Transform data dictionary to Recharts format."""
        chart_data = []
        
        for key, value in data_dict.items():
            try:
                if self._is_numeric_key(key):
                    # It's a numeric timestamp
                    chart_data.append(self._create_time_point(key, value))
                else:
                    # It's a category/string key
                    chart_data.append(self._create_category_point(key, value))
            except (ValueError, TypeError):
                # If conversion fails, keep as string
                chart_data.append({"category": key, "value": value, "label": key})
                
        return chart_data
    
    def _is_numeric_key(self, key: str) -> bool:
        """Check if a key is numeric (for timestamps)."""
        return key.isdigit() or (key.startswith("-") and key[1:].isdigit())
    
    def _create_time_point(self, key: str, value: Any) -> Dict[str, Any]:
        """Create a time-series data point."""
        return {"timestamp": int(key), "value": float(value), "date": key}
    
    def _create_category_point(self, key: str, value: Any) -> Dict[str, Any]:
        """Create a categorical data point."""
        return {
            "category": key,
            "value": self._convert_to_float_if_possible(value),
            "label": key,
        }
    
    def _convert_to_float_if_possible(self, value: Any) -> Union[float, Any]:
        """Convert value to float if possible, otherwise return as is."""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str) and value.replace(".", "", 1).isdigit():
            return float(value)
        return value


class DashboardWithGraphsSerializer(serializers.ModelSerializer):
    """Serializer for Dashboard with its associated Graphs"""

    graphs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Dashboard
        # Explicitly list fields in the desired order
        fields = [
            "id",
            "type_dashboard",
            "insight",
            "created_at",
            "graphs",
        ]
        read_only_fields = ["created_at"]

    def get_graphs(self, obj) -> List[Dict[str, Any]]:
        """Get all graphs associated with this dashboard.
        
        This method uses select_related to optimize the query.
        
        Args:
            obj: The Dashboard model instance
            
        Returns:
            Serialized graph data
        """
        graphs = Graph.objects.filter(dashboard=obj).order_by('-created_at')
        return GraphSerializer(graphs, many=True).data
