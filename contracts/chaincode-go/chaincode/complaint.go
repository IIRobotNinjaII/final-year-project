package chaincode

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

type Asset struct {
	ID                  string    `json:"id"`
	Attributes          string    `json:"attributes"`
	Description         string    `json:"description"`
	DescriptionUserCopy string    `json:"description_user_copy"`
	CreatedAt           string 	  `json:"created_at"`
	Resolved            bool      `json:"resolved"`
	AuthorID            string    `json:"author_id"`
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, attributes string, description string, descriptionUserCopy string, authorID string,created_at string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	asset := Asset{
		ID:             		id,
		Attributes:         	attributes,
		Description:        	description,
		DescriptionUserCopy:    descriptionUserCopy,
		CreatedAt: 				created_at,
		Resolved:				false,
		AuthorID:				authorID,
	}
	assetJSON, err := json.Marshal(asset)

	if err != nil {
        return fmt.Errorf("joining error %s", err)
    }

	if err := ctx.GetStub().PutState(id, assetJSON); err != nil {
        return err
    }

	if err := s.CreateIndex(ctx, "authorID~id", []string{authorID, id}); err != nil {
        return err
    }

	return nil
}

func (s *SmartContract) CreateIndex(ctx contractapi.TransactionContextInterface, indexName string, attributes []string) error {
    indexKey, err := ctx.GetStub().CreateCompositeKey(indexName, attributes)
    if err != nil {
        return err
    }

    // Save index to the ledger
    return ctx.GetStub().PutState(indexKey, []byte{0x00})
}

func (s *SmartContract) QueryAssetsByAuthorID(ctx contractapi.TransactionContextInterface, authorID string) ([]*Asset, error) {
    resultsIterator, err := ctx.GetStub().GetStateByPartialCompositeKey("authorID~id", []string{authorID})
    if err != nil {
        return nil, err
    }
    defer resultsIterator.Close()

    var assets []*Asset
    for resultsIterator.HasNext() {
        queryResponse, err := resultsIterator.Next()
        if err != nil {
            return nil, err
        }

        // Retrieve asset ID from composite key
        _, compositeKeyParts, err := ctx.GetStub().SplitCompositeKey(queryResponse.Key)
        if err != nil {
            return nil, err
        }
        assetID := compositeKeyParts[1]

        // Retrieve asset details using asset ID
        asset, err := s.ReadAsset(ctx, assetID)
        if err != nil {
            return nil, err
        }

        assets = append(assets, asset)
    }

    return assets, nil
}


// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// UpdateAsset updates an existing asset in the world state with provided parameters.
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, id string) error {
	existingAssetJSON, err := ctx.GetStub().GetState(id)
    if err != nil {
        return err
    }
    if existingAssetJSON == nil {
        return fmt.Errorf("failed to retrieve asset %s", id)
    }

	var existingAsset Asset
    if err := json.Unmarshal(existingAssetJSON, &existingAsset); err != nil {
        return err
    }

	existingAsset.Resolved = true

    updatedAssetJSON, err := json.Marshal(existingAsset)
    if err != nil {
        return err
    }

    return ctx.GetStub().PutState(id, updatedAssetJSON)
	
}

// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, id string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	return ctx.GetStub().DelState(id)
}


// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}
