import pandas as pd
from typing import Dict

class DataSanitizer:
    def __init__(self):
        self.token_map: Dict[str, str] = {}
        self.reverse_map: Dict[str, str] = {}
        self.client_counter = 1

    def _get_or_create_token(self, original_name: str) -> str:
        if original_name not in self.token_map:
            token = f"<CLIENT_{self.client_counter:03d}>"
            self.token_map[original_name] = token
            self.reverse_map[token] = original_name
            self.client_counter += 1
        return self.token_map[original_name]

    def sanitize_dataframe(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Replaces actual client names with zero-trust tokens in a pandas DataFrame.
        """
        sanitized_df = df.copy()
        if target_column in sanitized_df.columns:
            sanitized_df[target_column] = sanitized_df[target_column].apply(self._get_or_create_token)
        return sanitized_df

    def rehydrate_text(self, text: str) -> str:
        """
        Swaps tokens back to actual client names for the final output.
        """
        rehydrated_text = text
        for token, original_name in self.reverse_map.items():
            rehydrated_text = rehydrated_text.replace(token, original_name)
        return rehydrated_text
