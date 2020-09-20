// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "AssetManagerStyle.h"

class FAssetManagerCommands : public TCommands<FAssetManagerCommands>
{
public:

	FAssetManagerCommands()
		: TCommands<FAssetManagerCommands>(TEXT("AssetManager"), NSLOCTEXT("Contexts", "AssetManager", "AssetManager Plugin"), NAME_None, FAssetManagerStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
