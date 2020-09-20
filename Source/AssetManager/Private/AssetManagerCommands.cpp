// Copyright Epic Games, Inc. All Rights Reserved.

#include "AssetManagerCommands.h"

#define LOCTEXT_NAMESPACE "FAssetManagerModule"

void FAssetManagerCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "AssetManager", "Execute AssetManager action", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
